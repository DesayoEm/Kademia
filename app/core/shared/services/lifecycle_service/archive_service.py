from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy.orm.collections import InstrumentedList
from .dependency_config import DEPENDENCY_CONFIG
from ...exceptions import CascadeArchivalError


class ArchiveService:
    """
    Service for managing entity archival and checking dependencies before archival.
    Methods check if an entity can be safely archived by verifying that no active entities are referencing it.
    """

    def __init__(self, session: Session, current_user):
        """
        Initialize the archive service with a db session and user.

        Args:
            session (Session): SQLAlchemy db session
        """
        self.session = session
        self.current_user = current_user


    def check_active_dependencies_exists(
            self, entity_model, target_id: UUID,
            is_archived_field: str = "is_archived") -> List[str]:
        """
        Check if any active entities are referencing the target entity using DEPENDENCY CONFIG
        Args:
            entity_model: SQLAlchemy model class for the entity type being checked
            target_id (UUID): The ID of the entity to check for dependencies
            is_archived_field (str): The field name used to determine if an entity is archived

        Returns:
            List[str]: Display names of entity types that have active dependencies
                       on the target entity. Empty list if no dependencies exist.
        """
        dependencies = DEPENDENCY_CONFIG.get(entity_model)
        failed = []

        for _, model_class, fk_field, display_name in dependencies:
            #fk based check
            table = model_class.__table__
            stmt = select(exists().where(
                 table.c[fk_field] == target_id,
                table.c[is_archived_field] == False
            ))

            if self.session.execute(stmt).scalar_one():
                failed.append(display_name)

        return failed



    def cascade_archive_object(self, entity_model, target_obj, reason: str) -> None:
        dependencies = DEPENDENCY_CONFIG.get(entity_model)

        for relationship_title, _, _, _ in dependencies:
            if not relationship_title:
                continue

            try:
                relationship_prop = getattr(type(target_obj), relationship_title).property
                backref = relationship_prop.back_populates

                if not backref:
                    raise ValueError(f"Relationship '{relationship_title}' must define back_populates.")

                related_attr = getattr(target_obj, relationship_title)

                if isinstance(related_attr, InstrumentedList):
                    for item in related_attr:
                        item.archive(self.current_user, reason)

                elif related_attr is not None:
                    related_attr.archive(self.current_user, reason)

            except Exception as e:
                self.session.rollback()
                raise CascadeArchivalError(f"[{relationship_title}] Cascade failed: {e}")

        try:
            target_obj.archive(self.current_user, reason)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise CascadeArchivalError(f"[{entity_model}] Failed to archive main object: {e}")



