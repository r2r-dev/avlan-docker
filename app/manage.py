from MySQLdb import (
    IntegrityError,
    OperationalError,
)

from click import (
    group,
    option,
)

from src.conf import (
    settings,
    defaults,
)
from src.utils.dao.AvlanSQLDao import AvlanSQLDao


@group()
def cli():
    pass


@cli.command()
@option(
    '--dump',
    help="Database dump file.",
    type=unicode,
    required=True,
)
def syncdb(dump):
    try:
        dao = AvlanSQLDao(
            host=settings.db_host,
            port=settings.db_port,
            username=settings.db_username,
            password=settings.db_password,
            database=settings.db_database,
            keepalive=True,
            autocommit=True,
        )
    except OperationalError:
        dao = AvlanSQLDao(
            host=settings.db_host,
            port=settings.db_port,
            username=settings.db_username,
            password=settings.db_password,
            keepalive=True,
            autocommit=True,
        )
        dao.raw_execute(
            'CREATE DATABASE IF NOT EXISTS `{0:s}`'.format(settings.db_database)
        )

        dao = AvlanSQLDao(
            host=settings.db_host,
            port=settings.db_port,
            username=settings.db_username,
            password=settings.db_password,
            database=settings.db_database,
            keepalive=True,
            autocommit=True,
        )

    with open(dump) as fd:
        sql_file = fd.read()

    # all SQL commands (split on ';')
    sql_commands = sql_file.split(';')

    for sql_command in sql_commands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        dao.raw_execute(sql_command)

    for default_object in defaults.create_defaults():
        try:
            dao.save(
                default_object,
                ignore_none=False,
            )
        except IntegrityError, e:
            continue


if __name__ in '__main__':
    cli()
