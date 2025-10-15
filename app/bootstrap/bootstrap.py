
from app.bootstrap.seed_role_permissions import (
    seed_roles, seed_super_user_permissions, seed_student_permissions, seed_guardian_permissions
)
from app.bootstrap.seed_users import seed_super_user
from app.bootstrap.init_system_user import init_system_user_and_role
from app.bootstrap.seed_permissions import seed_permissions
from app.bootstrap.init_tables import create_tables

def run_bootstrap():
    try:
        # create_tables()
        # init_system_user_and_role()
        seed_roles()
        # seed_super_user()

        # seed_permissions()
        # seed_super_user_permissions()
        # seed_student_permissions()
        # seed_guardian_permissions()

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")



if __name__ == '__main__':
    run_bootstrap()