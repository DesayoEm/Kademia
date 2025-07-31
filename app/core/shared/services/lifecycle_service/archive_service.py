from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from .dependency_config import DEPENDENCY_CONFIG


class ArchiveService:
    """
    Service for managing entity archival and checking dependencies before archival.
    Methods check if an entity can be safely archived by verifying that no active entities are referencing it.
    """

    def __init__(self, session: Session):
        """
        Initialize the archive service with a db session.

        Args:
            session (Session): SQLAlchemy db session
        """
        self.session = session


    def check_active_dependencies_exists(
            self, entity_model, target_id: UUID,
            is_archived_field: str = "is_archived") -> List[str]:
        """
        Check if any active entities are referencing the target entity.

        Examines configured dependency relationships to see if any  non-archived entities reference the target entity.

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

        for relationship_title, model_class, fk_field, display_name in dependencies:
            #fk based check
            if fk_field:
                table = model_class.__table__
                stmt = select(exists().where(
                    table.c[fk_field] == target_id,
                    table.c[is_archived_field] == False
                ))

            else:
                # relationship based check
                related_attr = getattr(entity_model, relationship_title)
                related_cls = related_attr.property.mapper.class_
                backref = related_attr.property.back_populates

                if not backref:
                    raise ValueError(f"Relationship '{relationship_title}' must define back_populates.")

                if related_attr.property.uselist:
                    stmt = select(exists().where(
                        getattr(related_cls, backref.any(
                            id = target_id,
                            **{is_archived_field: False}
                        ))
                    ))
                else:
                    stmt = select(exists().where(
                        getattr(related_cls, backref).has(
                        id=target_id,
                        **{is_archived_field: False}
                        )
                    ))

            if self.session.execute(stmt).scalar_one():
                failed.append(display_name)

        return failed