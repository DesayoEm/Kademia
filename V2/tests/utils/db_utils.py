import alembic.config
from alembic import command

def migrate_to_db(script_location, alembic_ini_path,
                  connection = None, revision = 'head'):
    config=alembic.config.Config(alembic_ini_path)
    if connection is not None:
        config.attributes['connection'] = connection
        config.config_ini_section = 'testtrakademik'
        command.upgrade(config, revision)