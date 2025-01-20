import pytest
from app.database.models.common_imports import Base
from datetime import datetime, date, timezone
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.security.auth_models import Users, AccessLevelChanges
from app.database.models.profiles import Staff, Students, Parents, Admin, Educator
from app.database.models.documents import StudentDocuments
from app.database.models.organization import Departments, Classes, StaffDepartments, StaffRoles
from app.database.models.academic import Subjects, Grades, StudentSubjects
from app.database.models.data_enums import (
    UserType, AccessLevel, StaffType, Gender,
    DepartmentType, DepartmentCode, ClassLevel,
    ClassCode, StaffDepartmentName, SubjectGroup
)

#db setup
@pytest.fixture(scope="session")
def engine():
    """Create test database engine"""
    return create_engine("postgresql://postgres:password@localhost:5432/test")
    Base.metadata.create_all(engine)

    return engine

@pytest.fixture(scope="function")
def db_session(engine):
    """Create new database session for each test"""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

#Base fixtures for required entities
@pytest.fixture
def admin_user(db_session):
    """Create base admin user required for other operations"""
    user = Users(
        profile_id=uuid4(),
        user_type=UserType.ADMIN,
        password_hash="hashed_password",
        access_level=AccessLevel.SUPERUSER,
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def admin_profile(db_session, admin_user):
    """Create admin staff profile"""
    admin = Admin(
        id=uuid4(),
        profile_id=admin_user.profile_id,
        first_name="Admin",
        last_name="User",
        gender=Gender.MALE,
        staff_type=StaffType.ADMINISTRATOR,
        email_address="admin@school.com",
        phone="12345678901",
        address="123 Admin Street",
        date_joined=date.today(),
        access_level=AccessLevel.SUPERUSER,
        image_url="admin.jpg"
    )
    db_session.add(admin)
    db_session.commit()
    return admin

#Test StaffRoles
def test_create_staff_role(db_session, admin_profile):
    """Test creating a staff role"""
    role = StaffRoles(
        id=uuid4(),
        name="Principal",
        description="School Principal",
        created_by=admin_profile.id
    )
    db_session.add(role)
    db_session.commit()

    assert role.id is not None
    assert role.name == "Principal"
    assert role.created_by == admin_profile.id

#Test StaffDepartments
def test_create_staff_department(db_session, admin_profile):
    """Test creating a staff department"""
    dept = StaffDepartments(
        id=uuid4(),
        name=StaffDepartmentName.EDUCATION,
        description="Education Department",
        manager_id=admin_profile.id,
        created_by=admin_profile.id
    )
    db_session.add(dept)
    db_session.commit()

    assert dept.id is not None
    assert dept.name == StaffDepartmentName.EDUCATION
    assert dept.manager_id == admin_profile.id

#Test Academic Departments
def test_create_academic_department(db_session, admin_profile):
    """Test creating an academic department"""
    dept = Departments(
        id=uuid4(),
        name=DepartmentType.SCIENCE,
        code=DepartmentCode.SCI,
        description="Science Department",
        created_by=admin_profile.id
    )
    db_session.add(dept)
    db_session.commit()

    assert dept.id is not None
    assert dept.name == DepartmentType.SCIENCE
    assert dept.code == DepartmentCode.SCI

#test Classes
def test_create_class(db_session, admin_profile):
    """Test creating a class"""
    class_ = Classes(
        id=uuid4(),
        level=ClassLevel.SeniorSecondarySchool1,
        code=ClassCode.A,
        mentor_id=admin_profile.id,
        created_by=admin_profile.id
    )
    db_session.add(class_)
    db_session.commit()

    assert class_.id is not None
    assert class_.level == ClassLevel.SeniorSecondarySchool1
    assert class_.code == ClassCode.A

#Test Parent
@pytest.fixture
def parent_user(db_session):
    """Create parent user"""
    user = Users(
        profile_id=uuid4(),
        user_type=UserType.PARENT,
        password_hash="hashed_password",
        access_level=AccessLevel.USER,
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    db_session.commit()
    return user

def test_create_parent(db_session, parent_user, admin_profile):
    """Test creating a parent"""
    parent = Parents(
        id=uuid4(),
        profile_id=parent_user.profile_id,
        first_name="Parent",
        last_name="One",
        gender=Gender.FEMALE,
        email_address="parent@email.com",
        phone="12345678902",
        address="123 Parent Street",
        created_by=admin_profile.id,
        image_url="parent.jpg"
    )
    db_session.add(parent)
    db_session.commit()

    assert parent.id is not None
    assert parent.email_address == "parent@email.com"
    assert parent.profile_id == parent_user.profile_id

#Test Student
@pytest.fixture
def student_user(db_session):
    """Create student user"""
    user = Users(
        profile_id=uuid4(),
        user_type=UserType.STUDENT,
        password_hash="hashed_password",
        access_level=AccessLevel.USER,
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    db_session.commit()
    return user

def test_create_student(db_session, student_user, admin_profile, parent_user):
    """Test creating a student"""
    #create parent
    parent = Parents(
        id=uuid4(),
        profile_id=parent_user.profile_id,
        first_name="Parent",
        last_name="One",
        gender=Gender.FEMALE,
        email_address="parent@email.com",
        phone="12345678902",
        address="123 Parent Street",
        created_by=admin_profile.id,
        image_url="parent.jpg"
    )
    db_session.add(parent)

    #Create class
    class_ = Classes(
        id=uuid4(),
        level=ClassLevel.SeniorSecondarySchool1,
        code=ClassCode.A,
        mentor_id=admin_profile.id,
        created_by=admin_profile.id
    )
    db_session.add(class_)

    #Create department
    dept = Departments(
        id=uuid4(),
        name=DepartmentType.SCIENCE,
        code=DepartmentCode.SCI,
        description="Science Department",
        created_by=admin_profile.id
    )
    db_session.add(dept)
    db_session.commit()

    #Now create student
    student = Students(
        id=uuid4(),
        profile_id=student_user.profile_id,
        first_name="Student",
        last_name="One",
        gender=Gender.MALE,
        student_id="STU001",
        class_id=class_.id,
        department_id=dept.id,
        parent_id=parent.id,
        admission_date=date.today(),
        created_by=admin_profile.id,
        image_url="student.jpg"
    )
    db_session.add(student)
    db_session.commit()

    assert student.id is not None
    assert student.student_id == "STU001"
    assert student.class_id == class_.id
    assert student.department_id == dept.id
    assert student.parent_id == parent.id

#Test Subject
def test_create_subject(db_session, admin_profile):
    """Test creating a subject"""
    subject = Subjects(
        id=uuid4(),
        name="Physics",
        class_level=ClassLevel.SeniorSecondarySchool1,
        department_type=SubjectDepartmentType.SCIENCE,
        is_compulsory=True,
        created_by=admin_profile.id
    )
    db_session.add(subject)
    db_session.commit()

    assert subject.id is not None
    assert subject.name == "Physics"
    assert subject.department_type == SubjectDepartmentType.SCIENCE

# Test complex relationships
def test_assign_subject_to_student(db_session, admin_profile):
    """Test assigning a subject to a student"""
    # Create necessary entities first
    subject = Subjects(
        id=uuid4(),
        name="Physics",
        class_level=ClassLevel.SeniorSecondarySchool1,
        department_type=SubjectDepartmentType.SCIENCE,
        is_compulsory=True,
        created_by=admin_profile.id
    )
    db_session.add(subject)

    #Create student user
    student_user = Users(
        profile_id=uuid4(),
        user_type=UserType.STUDENT,
        password_hash="hashed_password",
        access_level=AccessLevel.USER,
        is_active=True,
        is_verified=True
    )
    db_session.add(student_user)

    #Create parent user and profile
    parent_user = Users(
        profile_id=uuid4(),
        user_type=UserType.PARENT,
        password_hash="hashed_password",
        access_level=AccessLevel.USER,
        is_active=True,
        is_verified=True
    )
    db_session.add(parent_user)

    parent = Parents(
        id=uuid4(),
        profile_id=parent_user.profile_id,
        first_name="Parent",
        last_name="One",
        gender=Gender.FEMALE,
        email_address="parent2@email.com",
        phone="12345678903",
        address="123 Parent Street",
        created_by=admin_profile.id,
        image_url="parent.jpg"
    )
    db_session.add(parent)

    #Create class and department
    class_ = Classes(
        id=uuid4(),
        level=ClassLevel.SeniorSecondarySchool1,
        code=ClassCode.A,
        mentor_id=admin_profile.id,
        created_by=admin_profile.id
    )
    db_session.add(class_)

    dept = Departments(
        id=uuid4(),
        name=DepartmentType.SCIENCE,
        code=DepartmentCode.SCI,
        description="Science Department",
        created_by=admin_profile.id
    )
    db_session.add(dept)

    #Create student
    student = Students(
        id=uuid4(),
        profile_id=student_user.profile_id,
        first_name="Student",
        last_name="Two",
        gender=Gender.MALE,
        student_id="STU002",
        class_id=class_.id,
        department_id=dept.id,
        parent_id=parent.id,
        admission_date=date.today(),
        created_by=admin_profile.id,
        image_url="student.jpg"
    )
    db_session.add(student)
    db_session.commit()

    #assign subject to student
    student_subject = StudentSubjects(
        id=uuid4(),
        student_id=student.id,
        subject_id=subject.id,
        academic_year=2025,
        term="FIRST",
        is_active=True,
        title="Physics 101",
        created_by=admin_profile.id
    )
    db_session.add(student_subject)
    db_session.commit()

    assert student_subject.id is not None
    assert student_subject.student_id == student.id
    assert student_subject.subject_id == subject.id