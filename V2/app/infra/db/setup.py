from db_config import engine
from V2.app.core.shared.models.common_imports import Base
from V2.app.core.auth.models.auth import AccessLevelChange
from V2.app.core.documents.models.documents import StudentDocument, StudentAward
from V2.app.core.transfer.models.transfer import DepartmentTransfer
from V2.app.core.assessment.models.assessment import Grade, TotalGrade
from V2.app.core.identity.models.student import Student
from V2.app.core.identity.models.guardian import Guardian

def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)

create_tables()