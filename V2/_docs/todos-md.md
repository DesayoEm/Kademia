# Technical Debt & TODOS

## Authentication & Audit Trail
**Priority: High**  
**Target Resolution: Before Production**

### Current Implementation
- Using SYSTEM_USER_ID (00000000-0000-0000-0000-000000000000) for all audit trails
- Affects created_by and last_modified_by fields across all models

### Required Changes
1. Implement authentication system
   - JWT token handling
   - User session management
   - Password hashing and validation

2. Service Layer Refactoring
   - Inject user context into service constructors
   - Update BaseService to use real user IDs
   - Add permission validation hooks

3. Database Considerations
   - Will require full database reset before production


## Future Enhancements

### RBAC Implementation
**Priority: Medium**  
**Target: Post-Authentication**

- Role hierarchy definition
- Permission granularity decisions
- Resource-level access control
- UI considerations for role-based content display

### Audit Trail Enhancement
**Priority: Low**  
**Target: Post-RBAC**

- Consider audit trail versioning
- Add reason tracking for modifications
- Implement audit log querying system

## Development Guidelines

1. Mark temporary solutions with TODO comments:
```python
# TODO(AUTH-123): Replace system users with actual users context
self.current_user_id = SYSTEM_USER_ID
```

## Issue Tracking
- AUTH-123: Implement authentication system
- RBAC-456: Design and implement role-based access control
- AUDIT-789: Enhance audit trail system

---
*Remember to update this document as new technical debt is identified or existing items are resolved.*