from functools import wraps
from app.core.shared.exceptions import PermissionHandlerError
from app.core.shared.models.enums import Resource, Action
from app.core.rbac.services.permission_service import PermissionService
from uuid import UUID


def require_permission(
    resource: Resource, action: Action, resource_id: UUID | None = None
):
    """
    Decorator that enforces permission checks on route handlers.

    Extracts the authenticated user and database session from the route's
    injected factory or service dependency, then verifies the user has
    the required permission before executing the route handler.

    Args:
        resource: The Resource enum value being accessed (e.g., Resource.STUDENT).
        action: The Action enum value being performed (e.g., Action.UPDATE).
        resource_id: Optional UUID of the specific resource instance for
            contextual access checks. If None, only role-based permission
            is verified.

    Returns:
        Callable: A decorator function that wraps the route handler.

    Raises:
        PermissionHandlerError: If the route handler doesn't have a 'factory'
            or 'service' keyword argument, or if that handler lacks 'session'
            and 'current_user' attributes.
        AccessDenied: Propagated from PermissionService.check_permission if
            the user lacks the required permission.

    Example:
        @router.put("/students/{student_id}")
        @require_permission(Resource.STUDENT, Action.UPDATE)
        def update_student(
            student_id: UUID,
            data: UpdateStudentSchema,
            factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
        ):
            return factory.update_student(student_id, data)

        With specific resource_id (for contextual checks)
        @router.get("/grades/{grade_id}")
        @require_permission(Resource.GRADE, Action.READ, resource_id=???)
        def get_grade(...):
            ...

    Note:
        The resource_id parameter is captured at decoration time, not runtime.
        For dynamic resource IDs (e.g., from path parameters), consider passing
        resource_id=None here and handling contextual checks within the route
        or service layer, or refactoring to extract resource_id from kwargs.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = kwargs.get("factory") or kwargs.get("service")
            if not handler:
                raise PermissionHandlerError(
                    "No factory or service found in route parameters"
                )

            if not hasattr(handler, "session") or not hasattr(handler, "current_user"):
                raise PermissionHandlerError(
                    "Handler must have session and current_user attributes"
                )

            permission_service = PermissionService(
                session=handler.session, current_user=handler.current_user
            )
            permission_service.check_permission(
                user=handler.current_user,
                resource=resource,
                action=action,
                resource_id=resource_id,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator
