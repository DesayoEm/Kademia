"""
Foreign Key Error Map
This file maps each factory class to a dictionary of foreign key constraint names
and their corresponding (model, attribute, user-facing label) tuples.
Format:
    {
        FactoryClass: {
            "fk_constraint_name": (RelatedModel, attr_name_on_obj, user_friendly_label)
        }
    }
Usage:
    - Inline for simple factories with 1-2 constraints
    - With helper (`resolve_fk_violation(...)`) for factories with 3+ FK constraints
"""

from ....database.models import *
from ...factories.student_organization import  classes
from ...factories.staff_organization import qualification

#fk_key: (model, attr, label)
fk_error_map = {
    "common": {
        "staff_created_by": (Staff, "created_by", "Creator"),
        "staff_last_modified_by": (Staff, "last_modified_by", "Last Modifier"),
        "staff_archived_by": (Staff, "archived_by", "Archiver"),
    },

    qualification.QualificationFactory: {
        "fk_educator_qualifications_educators_educator_id": (Educator, "educator_id", "Educator")

    },

    classes.ClassFactory: {
        "fk_classes_academic_levels_level_id": (AcademicLevel, "level_id", "Level")
    }
}
