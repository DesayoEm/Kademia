from db_config import engine
from app.core.shared.models.common_imports import Base
from app.core.auth.models.auth import AccessLevelChange
from app.core.documents.models.documents import StudentDocument, StudentAward
from app.core.transfer.models.transfer import DepartmentTransfer
from app.core.assessment.models.assessment import Grade, TotalGrade
from app.core.identity.models.student import Student
from app.core.identity.models.guardian import Guardian

def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)

if __name__ =='__main__':
    create_tables()