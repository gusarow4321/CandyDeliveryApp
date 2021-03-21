import argparse
import logging
import os
from sys import argv

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_sqlalchemy import DBSessionMiddleware
from configargparse import ArgumentParser
from setproctitle import setproctitle

from candy.api.validation_handler import validation_exc_handler

from candy.utils.arg_parse import clear_environ, positive_int
from candy.utils.db import DEFAULT_DB_URL

from candy.api.routers.couriers import router as couriers_router
from candy.api.routers.orders import router as orders_router


ENV_VAR_PREFIX = 'CANDY_'


parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX, allow_abbrev=False,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

group = parser.add_argument_group('API Options')
group.add_argument('--address', default='0.0.0.0', help='IPv4/IPv6 address API server would listen on')
group.add_argument('--port', type=positive_int, default=8081, help='TCP port API server would listen on')

group = parser.add_argument_group('PostgreSQL options')
group.add_argument('--db-url', type=str, default=DEFAULT_DB_URL, help='URL to use to connect to the database')

group = parser.add_argument_group('Logging options')
group.add_argument('--log-level', default='info', choices=('debug', 'info', 'warning', 'error', 'fatal'))


def create_app(db_url) -> FastAPI:
    app = FastAPI()
    app.add_middleware(DBSessionMiddleware, db_url=db_url, engine_args={'connect_args': {"options": "-c timezone=utc"}})

    app.add_exception_handler(RequestValidationError, handler=validation_exc_handler)

    app.include_router(couriers_router)
    app.include_router(orders_router)

    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    args = parser.parse_args()

    clear_environ(lambda i: i.startswith(ENV_VAR_PREFIX))

    setproctitle(os.path.basename(argv[0]))

    app = create_app(args.db_url)

    uvicorn.run(app, host=args.address, port=args.port)


if __name__ == '__main__':
    main()
