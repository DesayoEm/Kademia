from functools import wraps
from app.core.shared.exceptions import PermissionHandlerError
from app.core.shared.models.enums import Resource, Action
from app.core.rbac.services.permission_service import PermissionService
from uuid import UUID


def require_permission(
    resource: Resource, action: Action, resource_id: UUID | None = None
):
    """
    Decorator that checks if the current user has permission to perform
    an action on a resource.
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
