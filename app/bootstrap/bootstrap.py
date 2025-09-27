from app.bootstrap.python_scripts.init_roles import init_super_user_permissions
from app.bootstrap.python_scripts.init_user import init_system_user, init_roles
from app.bootstrap.python_scripts.init_permissions import init_permissions
from app.bootstrap.python_scripts.init_tables import create_tables

init_system_user()
def run_bootstrap():
    try:
        create_tables()
        init_roles()
        init_system_user()
        init_permissions()
        init_super_user_permissions()

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")



if __name__ == '__main__':
    run_bootstrap()