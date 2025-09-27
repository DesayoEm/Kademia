from app.bootstrap.python_scripts.init_user import create_user, create_role
from app.bootstrap.python_scripts.permissions import create_permissions
from app.bootstrap.python_scripts.roles import create_roles
from app.bootstrap.python_scripts.setup import create_tables
from app.bootstrap.python_scripts.matrix import matrix

create_user()
def run_bootstrap():
    try:
        create_tables()
        create_user()
        create_role()
        create_permissions()
        create_roles()

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")




if __name__ == '__main__':
    run_bootstrap()