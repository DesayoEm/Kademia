import alembic.config
from alembic import command
import os

def migrate_to_db(script_location, alembic_ini_path, connection=None, revision='head'):
    print(f"Looking for migrations in: {os.path.abspath('app/database/migrations/versions')}")
    print("Available migrations:", os.listdir('app/database/migrations/versions'))

    if connection is not None:
        try:

            print("Creating tables directly via SQLAlchemy...")
            from V2.app.database.models.common_imports import Base
            Base.metadata.create_all(bind=connection)
            print("Tables created successfully")


            config = alembic.config.Config(alembic_ini_path)
            config.config_ini_section = 'testtrakademik'
            config.set_main_option('script_location', 'app/database/migrations')
            config.attributes['connection'] = connection

            command.stamp(config, "head")  # Mark as migrated to head
            print("Database stamped at head revision")

        except Exception as e:
            print(f"Error during database setup: {str(e)}")
            raise