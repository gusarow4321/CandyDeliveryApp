import argparse
import logging
import os
from sys import argv

import uvicorn
from fastapi import FastAPI, Depends
from configargparse import ArgumentParser
from setproctitle import setproctitle

from candy.utils.arg_parse import clear_environ, positive_int
from candy.utils.db import DEFAULT_DB_URL

from candy.db.session import create_session
from candy.api.routers.couriers import router as couriers_router
from candy.api.routers.orders import router as orders_router


FastAPI()

ENV_VAR_PREFIX = 'CANDY_'


parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX, allow_abbrev=False,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

group = parser.add_argument_group('API Options')
group.add_argument('--address', default='0.0.0.0', help='IPv4/IPv6 address API server would listen on')
group.add_argument('--port', type=positive_int, default=8081, help='TCP port API server would listen on')

group = parser.add_argument_group('PostgreSQL options')
group.add_argument('--pg-url', type=str, default=DEFAULT_DB_URL, help='URL to use to connect to the database')

group = parser.add_argument_group('Logging options')
group.add_argument('--log-level', default='info', choices=('debug', 'info', 'warning', 'error', 'fatal'))


def main():
    logging.basicConfig(level=logging.DEBUG)

    args = parser.parse_args()

    clear_environ(lambda i: i.startswith(ENV_VAR_PREFIX))

    # В списке процессов намного удобнее видеть название текущего приложения
    setproctitle(os.path.basename(argv[0]))

    app = FastAPI()

    session_local = create_session(args.pg_url)

    def get_db():
        db = session_local()
        try:
            yield db
        finally:
            db.close()

    app.include_router(couriers_router,
                       prefix="/couriers",
                       tags=["couriers"],
                       dependencies=[Depends(get_db)],)
    app.include_router(orders_router,
                       prefix="/orders",
                       tags=["orders"],
                       dependencies=[Depends(get_db)],)

    uvicorn.run(app, host=args.address, port=args.port)


if __name__ == '__main__':
    main()
