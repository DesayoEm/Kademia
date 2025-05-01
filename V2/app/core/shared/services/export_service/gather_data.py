from V2.app.core.shared.exceptions.export_errors import UnimplementedGathererError
from ....staff_management.models.staff_management import StaffDepartment, StaffRole, EducatorQualification
from ....academic_structure.models.academic_structure import StudentDepartment, Classes, AcademicLevel
from ....transfer.models.transfer import StudentDepartmentTransfer, ClassTransfer
from ....assessment.models.assessment import Grade, TotalGrade,Repetition
from ....curriculum.models.curriculum import SubjectEducator, StudentSubject, Subject, AcademicLevelSubject
from ....transfer.models.transfer import StudentDepartmentTransfer, ClassTransfer
from ....documents.models.documents import StudentDocument, StudentAward
from ....auth.models.auth import AccessLevelChange
from ....identity.models.staff import Educator, AdminStaff, SupportStaff
from ....identity.models.student import Student
from ....identity.models.guardian import Guardian

from .gatherers.identity.staff_gatherer import StaffGatherer
from .gatherers.identity.student_gatherer import StudentGatherer
from .gatherers.identity.guardian_gatherer import GuardianGatherer
from .gatherers.staff_management.staff_management import StaffOrganizationGatherer
from .gatherers.academic_structure.academic_structure import AcademicStructureGatherer


class GatherData:
    def __init__(self):
        self.staff_gatherer = StaffGatherer()
        self.guardian_gatherer = GuardianGatherer()
        self.student_gatherer = StudentGatherer()
        self.staff_org_gatherer = StaffOrganizationGatherer()
        self.academic_gatherer = AcademicStructureGatherer()

        self.gatherers = {
            # Identity
            AdminStaff: self.staff_gatherer.gather_admin_staff_data,
            SupportStaff: self.staff_gatherer.gather_support_staff_data,
            Educator: self.staff_gatherer.gather_educator_data,

            Student: self.student_gatherer.gather_student_data,
            Guardian: self.guardian_gatherer.gather_guardian_data,

            # Academic structure domain
            AcademicLevel: self.academic_gatherer.gather_academic_level_data,
            Classes: self.academic_gatherer.gather_class_data,
            StudentDepartment: self.academic_gatherer.gather_department_data,


            # Staff Organization domain
            StaffRole: self.staff_org_gatherer.gather_role_data,
            StaffDepartment: self.staff_org_gatherer.gather_department_data,
            EducatorQualification: self.staff_org_gatherer.gather_qualification_data,

            # # Documents domain
            # StudentDocument: self.student_gatherer.gather_student_document_data,
            # StudentAward: self.student_gatherer.gather_student_award_data,
            #
            #
            #
            # # Assessment domain
            # Grade: self.academic_gatherer.gather_grade_data,
            # TotalGrade: self.academic_gatherer.gather_total_grade_data,
        }

    def gather(self, entity) -> tuple:
        """Dispatch to the correct gather method based on entity type."""
        entity_type = type(entity)
        gather_function = self.gatherers.get(entity_type)

        if not gather_function:
            raise UnimplementedGathererError(entity=entity_type.__name__)

        return gather_function(entity)