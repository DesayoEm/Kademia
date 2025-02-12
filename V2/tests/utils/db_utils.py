import alembic.config
from alembic import command

def migrate_to_db(script_location, alembic_ini_path, connection = None, revision = 'head'):
    try:
        # Try direct table creation first
        from V2.app.database.models.common_imports import Base
        Base.metadata.create_all(bind=connection)

        # Then try migrations
        config = alembic.config.Config(alembic_ini_path)
        config.config_ini_section = 'testtrakademik' #TO fix why migrations wont work
        config.set_main_option('script_location', 'app/database/migrations')
        config.attributes['connection'] = connection

        command.stamp(config, revision)
        print("Database stamped at latest revision")

    except Exception as e:
        print(f"Migration error: {e}")
        raise