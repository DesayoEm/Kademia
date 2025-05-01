from V2.app.core.shared.exceptions.export_errors import UnimplementedGathererError
from ....staff_management.models.staff_management import StaffDepartment, StaffRole, EducatorQualification
from ....academic_structure.models.academic_structure import StudentDepartment, Classes, AcademicLevel
from ....identity.models.staff import Educator, AdminStaff, SupportStaff
from ....identity.models.student import Student
from ....identity.models.guardian import Guardian
from ....assessment.models.assessment import Grade, TotalGrade, Repetition
from ....curriculum.models.curriculum import Subject, AcademicLevelSubject, StudentSubject, SubjectEducator
from ....transfer.models.transfer import StudentDepartmentTransfer, ClassTransfer
from ....documents.models.documents import StudentDocument, StudentAward
from ....auth.models.auth import AccessLevelChange

from .gatherers.identity.staff_gatherer import StaffGatherer
from .gatherers.identity.student_gatherer import StudentGatherer
from .gatherers.identity.guardian_gatherer import GuardianGatherer
from V2.app.core.shared.services.export_service.gatherers.staff_management import StaffOrganizationGatherer
from V2.app.core.shared.services.export_service.gatherers.academic_structure import AcademicStructureGatherer
from V2.app.core.shared.services.export_service.gatherers.curriculum import CurriculumGatherer
from V2.app.core.shared.services.export_service.gatherers.assessment import AssessmentGatherer
from V2.app.core.shared.services.export_service.gatherers.transfer import TransferGatherer
from V2.app.core.shared.services.export_service.gatherers.documents import DocumentsGatherer
from V2.app.core.shared.services.export_service.gatherers.auth import AuthGatherer


class GatherData:
    def __init__(self):
        self.staff_gatherer = StaffGatherer()
        self.guardian_gatherer = GuardianGatherer()
        self.student_gatherer = StudentGatherer()
        self.staff_org_gatherer = StaffOrganizationGatherer()
        self.academic_gatherer = AcademicStructureGatherer()
        self.curriculum_gatherer = CurriculumGatherer()
        self.assessment_gatherer = AssessmentGatherer()
        self.transfer_gatherer = TransferGatherer()
        self.document_gatherer = DocumentsGatherer()
        self.auth_gatherer = AuthGatherer()

        self.gatherers = {
            # Identity
            AdminStaff: self.staff_gatherer.gather_admin_staff_data,
            SupportStaff: self.staff_gatherer.gather_support_staff_data,
            Educator: self.staff_gatherer.gather_educator_data,
            Student: self.student_gatherer.gather_student_data,
            Guardian: self.guardian_gatherer.gather_guardian_data,

            # Academic Structure
            AcademicLevel: self.academic_gatherer.gather_academic_level_data,
            Classes: self.academic_gatherer.gather_class_data,
            StudentDepartment: self.academic_gatherer.gather_department_data,

            # Staff Organization
            StaffRole: self.staff_org_gatherer.gather_role_data,
            StaffDepartment: self.staff_org_gatherer.gather_department_data,
            EducatorQualification: self.staff_org_gatherer.gather_qualification_data,

            # Curriculum
            Subject: self.curriculum_gatherer.gather_subject_data,
            AcademicLevelSubject: self.curriculum_gatherer.gather_academic_level_subject_data,
            StudentSubject: self.curriculum_gatherer.gather_student_subject_data,
            SubjectEducator: self.curriculum_gatherer.gather_subject_educator_data,

            # Assessment
            Grade: self.assessment_gatherer.gather_grade_data,
            TotalGrade: self.assessment_gatherer.gather_total_grade_data,
            Repetition: self.assessment_gatherer.gather_repetition_data,

            # Transfers
            StudentDepartmentTransfer: self.transfer_gatherer.gather_student_department_transfer_data,
            ClassTransfer: self.transfer_gatherer.gather_class_transfer_data,

            # Documents
            StudentDocument: self.document_gatherer.gather_student_document_data,
            StudentAward: self.document_gatherer.gather_student_award_data,

            # Auth Logs
            AccessLevelChange: self.auth_gatherer.gather_access_level_change_data,
        }

    def gather(self, entity) -> tuple:
        """Dispatch to the correct gather method based on entity type."""
        entity_type = type(entity)
        gather_function = self.gatherers.get(entity_type)

        if not gather_function:
            raise UnimplementedGathererError(entity=entity_type.__name__)

        return gather_function(entity)
