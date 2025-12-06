from uuid import UUID
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.core.identity.models.guardian import Guardian
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository


class GuardianService:
    def __init__(self, session: Session, current_user=None):
        self.session = session
        self.current_user = current_user
        self.repository = SQLAlchemyRepository(Guardian, self.session)

    def archive_orphaned_guardians(self, reason: str):
        from app.core.identity.models.student import Student

        orphaned_guardians = (
            self.session.query(Guardian)
            .filter(
                and_(
                    Guardian.is_archived == False,
                    ~Guardian.wards.any(Student.is_archived == False),
                )
            )
            .all()
        )

        for guardian in orphaned_guardians:
            guardian.archive(self.current_user, reason)
            self.session.commit()
