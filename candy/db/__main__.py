import argparse
import logging
import os

from alembic.config import CommandLine

from candy.utils.db import DEFAULT_DB_URL, make_alembic_config


def main():
    logging.basicConfig(level=logging.DEBUG)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    alembic.parser.add_argument(
        '--db-url', default=os.getenv('CD_DB_URL', DEFAULT_DB_URL), help='Database URL [env var: CD_DB_URL]'
    )

    options = alembic.parser.parse_args()
    if 'cmd' not in options:
        alembic.parser.error('too few arguments')
        exit(128)
    else:
        config = make_alembic_config(options)
        exit(alembic.run_cmd(config, options))


if __name__ == '__main__':
    main()
