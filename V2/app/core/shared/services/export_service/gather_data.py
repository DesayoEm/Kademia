from V2.app.core.shared.errors.export_errors import UnimplementedGathererError
from V2.app.database.models import *

from .gatherers.user.staff_gatherer import StaffGatherer
from .gatherers.user.student_gatherer import StudentGatherer
from .gatherers.user.guardian_gatherer import GuardianGatherer
from .gatherers.staff_organization.staff_organisation import StaffOrganizationGatherer
from .gatherers.academic_structure.academic_structure import AcademicStructureGatherer


class GatherData:
    def __init__(self):
        self.staff_gatherer = StaffGatherer()
        self.guardian_gatherer = GuardianGatherer()
        self.student_gatherer = StudentGatherer()
        self.staff_org_gatherer = StaffOrganizationGatherer()
        self.academic_gatherer = AcademicStructureGatherer()

        self.gatherers = {
            # User domain
            AdminStaff: self.staff_gatherer.gather_admin_staff_data,
            SupportStaff: self.staff_gatherer.gather_support_staff_data,
            Educator: self.staff_gatherer.gather_educator_data,

            Student: self.student_gatherer.gather_student_data,
            Guardian: self.student_gatherer.gather_student_data,

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