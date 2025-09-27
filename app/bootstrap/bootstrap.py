from app.bootstrap.python_scripts.init_user import create_user, create_role
from app.bootstrap.python_scripts.init_permissions import create_permissions
from app.bootstrap.python_scripts.init_tables import create_tables
from app.bootstrap.python_scripts.matrix import matrix

create_user()
def run_bootstrap():
    try:
        create_tables()
        create_role()
        create_user()
        create_permissions()
        # create_roles()

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")



if __name__ == '__main__':
    run_bootstrap()