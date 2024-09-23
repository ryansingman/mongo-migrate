"""
    Module: migration_cli.py
    Author: Rahul George
    
    Description:
        This module abstracts away all the CLI interactions.
        Every cli command will be added as an argparse sub-parser but in the end, it will call
         the MigrationManager class.
        The decision to go with argparse is to keep the tool dependency minimal.
    
    License:
    
    Created on: 14-08-2023
    
"""
import argparse
from dataclasses import dataclass
from typing import Optional

from mongo_migrate.migration_manager import MigrationManager


@dataclass
class Config:
    host: str
    port: int
    database: str
    username: Optional[str]
    password: Optional[str]


def subparser_for_create(subparsers):
    """Subparser for create command"""
    create_subparser = subparsers.add_parser('create', help='create a new migration')
    create_subparser.set_defaults(func=create_migration)

    _add_common_subparser_args(create_subparser)
    create_subparser.add_argument('--title', help='short title that will be used in the file name. Default: version', default='version', action='store', dest='title')
    create_subparser.add_argument('--message', help='short message that will be saved as a comment inside the migration file', required=True, action='store', dest='message')


def create_migration(args):
    """Entry point for create migration command"""
    config = Config(args.host, args.port, args.database)
    m = MigrationManager(config, args.migrations)
    m.create_migration(args.title, args.message)


def subparser_for_upgrade(subparsers):
    """Subparser for upgrade command"""
    upgrade_subparser = subparsers.add_parser('upgrade', help='upgrade the database to the target migration version')
    upgrade_subparser.set_defaults(func=migrate)

    _add_common_subparser_args(upgrade_subparser)
    upgrade_subparser.add_argument('--upto', help='target migration timestamp', action='store', dest='upto')
    upgrade_subparser.add_argument('--type', help=argparse.SUPPRESS, action='store', dest='type', default='upgrade')


def subparser_for_downgrade(subparsers):
    """Subparser for upgrade command"""
    upgrade_subparser = subparsers.add_parser('downgrade', help='downgrade the database to the target migration version')
    upgrade_subparser.set_defaults(func=migrate)

    _add_common_subparser_args(upgrade_subparser)
    upgrade_subparser.add_argument('--upto', help='target migration timestamp', action='store', dest='upto')
    upgrade_subparser.add_argument('--type', help=argparse.SUPPRESS, action='store', dest='type', default='downgrade')

    
def _add_common_subparser_args(subparser: argparse.ArgumentParser):
    subparser.add_argument('--host', help='the database host', action='store', dest='host')
    subparser.add_argument('--port', help='the database port', action='store', dest='port')
    subparser.add_argument('--username', help='the database username', action='store', dest='username', default=None)
    subparser.add_argument('--password', help='the database password', action='store', dest='password', default=None)
    subparser.add_argument('--database', help='the database name', action='store', dest='database')
    subparser.add_argument('--migrations', help='provide the folder to store migrations. By default looks for migrations/', default='migrations', action='store', dest='migrations')


def migrate(args):
    """Entry point for both upgrade and downgrade"""
    config = Config(args.host, args.port, args.database, args.username, args.password)
    m = MigrationManager(config, args.migrations)
    m.migrate(args.type, args.upto)


def parse_arguments():
    parser = argparse.ArgumentParser(prog='mongo-migrate')
    subparsers = parser.add_subparsers()

    # Add subparser methods below
    subparser_for_create(subparsers)
    subparser_for_upgrade(subparsers)
    subparser_for_downgrade(subparsers)

    # Generic parse call
    args = parser.parse_args()
    args.func(args)


def main():
    parse_arguments()


if __name__ == '__main__':
    main()
