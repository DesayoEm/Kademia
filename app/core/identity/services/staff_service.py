from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import update


from app.core.identity.factories.staff import StaffFactory
from app.core.identity.models.staff import Staff, Educator
from app.core.shared.exceptions import CascadeArchivalError
from app.core.shared.models.enums import StaffAvailability, StaffType
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService


class StaffService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.factory = StaffFactory(session, Staff, current_user= current_user)
        self.archive_service = ArchiveService(session, current_user=current_user)

    def unassign_staff_roles(self, staff_id: UUID):
        """Remove staff from manager, mentorship and supervision roles before archival"""
        from app.core.academic_structure.models import StudentDepartment, Classes
        from app.core.staff_management.models import StaffDepartment

        #set manager_id to NULL for any departments they manage
        manager_stmt = (
            update(StaffDepartment)
            .where(StaffDepartment.manager_id == staff_id)
            .values(manager_id=None)
        )


        #set mentor_id to NULL for any departments they mentor
        mentor_stmt = (
            update(StudentDepartment)
            .where(StudentDepartment.mentor_id == staff_id)
            .values(mentor_id=None)
        )

        #set supervisor_id to NULL for any classes they supervise
        supervisor_stmt = (
            update(Classes)
            .where(Classes.supervisor_id == staff_id)
            .values(supervisor_id=None)
        )

        self.session.execute(manager_stmt)
        self.session.execute(mentor_stmt)
        self.session.execute(supervisor_stmt)


    def cascade_staff_archive(self, staff_id: UUID, reason: str):
        staff = self.factory.get_staff(staff_id)

        try:
            self.unassign_staff_roles(staff_id)

            if staff.staff_type == StaffType.EDUCATOR:
                self.archive_service.cascade_archive_object(Educator, staff, reason)
            else:
                self.archive_service.cascade_archive_object(Staff, staff, reason)

        except Exception as e:
            self.session.rollback()
            raise CascadeArchivalError(str(e))


    def assign_role(self, staff_id: UUID, role_id: UUID | None = None):
        """Assign a role to staff member"""
        if not role_id:
            return self.factory.update_staff(staff_id, {"role_id": None})

        return self.factory.update_staff(staff_id, {"role_id": role_id})


    def assign_department(self, staff_id: UUID, department_id: UUID | None = None):
        """Assign a department to staff member"""
        if not department_id:
            return self.factory.update_staff(staff_id, {"department_id": None})

        return self.factory.update_staff(staff_id, {"department_id": department_id})


    def update_staff_availability(self, staff_id: UUID, availability: StaffAvailability):
        """Update staff availability status."""
        return self.factory.update_staff(staff_id, {"availability": availability.value})

