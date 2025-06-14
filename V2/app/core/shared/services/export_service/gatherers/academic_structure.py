from typing import Dict, Tuple, Any
from V2.app.core.academic_structure.models import (
    AcademicLevel, Classes, StudentDepartment
)


class AcademicStructureGatherer:
    """Gathers data for academic structure entities including academic levels, classes and student departments"""

    @staticmethod
    def gather_academic_level_data(level: AcademicLevel) -> Tuple[Dict[str, Any], str]:
        """Gather data for AcademicLevel entity."""
        file_name = f"AcademicLevel_{level.name}"

        return ({
                    "academic_level": {
                        "id": str(level.id),
                        "name": level.name,
                        "description": level.description,
                        "order": level.display_order,
                        "rank": level.promotion_rank,
                        "created_at": level.created_at,
                        "created_by": str(level.created_by) if level.created_by else None,
                        "last_modified_at": level.last_modified_at,
                        "last_modified_by": str(level.last_modified_by) if level.last_modified_by else None,
                    },
                    "classes": [
                        {
                            "id": str(class_.id),
                            "code": class_.code,
                            "supervisor": f"{class_.supervisor.first_name} {class_.supervisor.last_name}" if class_.supervisor else None,
                            "student_count": len(class_.students) if hasattr(class_, "students") else 0,
                        }
                        for class_ in level.classes
                    ],
                    "subjects": [
                        {
                            "id": str(level_subject.subject.id),
                            "name": level_subject.subject.name,
                            "is_elective": level_subject.is_elective,
                            "academic_session": level_subject.academic_session,
                            "educator": f"{level_subject.educator_id}" if level_subject.educator_id else None,
                        }
                        for level_subject in level.subjects
                    ],
                    "students": {
                        "count": len(level.students) if hasattr(level, "students") else 0,
                        "active_count": sum(1 for s in level.students if s.status == "ENROLLED") if hasattr(level,
                                                                                                            "students") else 0,
                    }
                }, file_name)


    @staticmethod
    def gather_class_data(self, class_: Classes) -> Tuple[Dict[str, Any], str]:
        """Gather data for Classes entity."""
        file_name = f"Class_{class_.academic_level.name}_{class_.code}" if class_.academic_level else f"Class_{class_.code}"

        students = class_.students if hasattr(class_, "students") else []

        return ({
                    "class": {
                        "id": str(class_.id),
                        "code": class_.code,
                        "order": class_.order,
                        "created_at": class_.created_at,
                        "created_by": str(class_.created_by) if class_.created_by else None,
                        "last_modified_at": class_.last_modified_at,
                        "last_modified_by": str(class_.last_modified_by) if class_.last_modified_by else None,
                    },
                    "academic_level": {
                        "id": str(class_.academic_level.id) if class_.academic_level else None,
                        "name": class_.academic_level.name if class_.academic_level else None,
                    },
                    "supervisor": {
                        "id": str(class_.supervisor.id) if class_.supervisor else None,
                        "name": f"{class_.supervisor.first_name} {class_.supervisor.last_name}" if class_.supervisor else None,
                    },
                    "representatives": {
                        "student_rep": {
                            "id": str(class_.student_rep.id) if class_.student_rep else None,
                            "name": f"{class_.student_rep.first_name} {class_.student_rep.last_name}" if class_.student_rep else None,
                        },
                        "assistant_rep": {
                            "id": str(class_.assistant_rep.id) if class_.assistant_rep else None,
                            "name": f"{class_.assistant_rep.first_name} {class_.assistant_rep.last_name}" if class_.assistant_rep else None,
                        }
                    },
                    "students": {
                        "count": len(students),
                        "gender_distribution": {
                            "male": sum(1 for s in students if s.gender == "MALE"),
                            "female": sum(1 for s in students if s.gender == "FEMALE"),
                        },
                        "status_distribution": {
                            "enrolled": sum(1 for s in students if s.status == "ENROLLED"),
                            "left": sum(1 for s in students if s.status == "LEFT"),
                            "graduated": sum(1 for s in students if s.status == "GRADUATED"),
                        }
                    }
                }, file_name)

    @staticmethod
    def gather_department_data(department: StudentDepartment) -> Tuple[Dict[str, Any], str]:
        """Gather data for StudentDepartment entity."""
        file_name = f"Department_{department.code}"

        students = department.students if hasattr(department, "students") else []

        return ({
                    "department": {
                        "id": str(department.id),
                        "name": department.name,
                        "code": department.code,
                        "description": department.description,
                        "created_at": department.created_at,
                        "created_by": str(department.created_by) if department.created_by else None,
                        "last_modified_at": department.last_modified_at,
                        "last_modified_by": str(department.last_modified_by) if department.last_modified_by else None,
                    },
                    "mentor": {
                        "id": str(department.mentor.id) if department.mentor else None,
                        "name": f"{department.mentor.first_name} {department.mentor.last_name}" if department.mentor else None,
                    },
                    "representatives": {
                        "student_rep": {
                            "id": str(department.student_rep_id) if department.student_rep_id else None,
                            "name": f"{department.student_rep.first_name} {department.student_rep.last_name}" if department.student_rep else None,
                        },
                        "assistant_rep": {
                            "id": str(department.assistant_rep_id) if department.assistant_rep_id else None,
                            "name": f"{department.assistant_rep.first_name} {department.assistant_rep.last_name}" if department.assistant_rep else None,
                        }
                    },
                    "students": {
                        "count": len(students),
                        "by_level": {
                            level.name: sum(1 for s in students if s.level and s.level.id == level.id)
                            for level in set(s.level for s in students if s.level)
                        },

                        "by_status": {
                            "enrolled": sum(1 for s in students if s.status == "ENROLLED"),
                            "left": sum(1 for s in students if s.status == "LEFT"),
                            "graduated": sum(1 for s in students if s.status == "GRADUATED"),
                        }
                    }
                }, file_name)