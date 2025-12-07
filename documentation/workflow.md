# Roadmap

### Phase 0: Foundation
- [x] PostgreSQL + SQLAlchemy 2.0 setup with Alembic migrations
- [x] Domain models with audit, timestamp, and archive mixins
- [x] Pydantic schemas for all entities

### Phase 1: Core Services
- [x] Repository + Factory + Service layer architecture
- [x] CRUD operations with pagination and filtering
- [x] Cascade archival with dependency awareness
- [x] Cascade deletion with integrity protection

### Phase 2: Data Integrity
- [x] FK/unique constraint violation handling
- [x] Archival cascade testing
- [x] Deletion blocking verification

### Phase 3: REST API
- [x] RESTful endpoint design with consistent status codes
- [x] Dynamic query filters
- [x] OpenAPI documentation
- [x] Standardized error responses

### Phase 4: Authentication
- [x] Password hashing + JWT tokens
- [x] Login/registration flows
- [x] Session management with Redis
- [x] Role and permission models

---

### Phase 4: Authorization (current)
- [x] Permission matrix (Resource × Action)
- [x] Role hierarchy
- [ ] Permission decorators for service methods
- [ ] Route-level authorization guards
- 

### Phase 5: Bulk Operations
- [ ] Batch create/update with validation
- [ ] Bulk archival and deletion
- [ ] Partial failure handling with rollback

### Phase 6: Background Processing
- [ ] Task queue infrastructure (Celery or RQ)
- [ ] Job status tracking and retries
- [ ] Email/SMS notification tasks

### Phase 7: Performance
- [ ] Query and index optimization
- [ ] Connection pooling tuning
- [ ] Response caching strategies

### Phase 8: Security Hardening
- [ ] Rate limiting (per-user and global)
- [ ] Security headers

### Phase 9: Testing
- [ ] Unit tests (models, services)
- [ ] Integration tests (API endpoints)
- [ ] Load and stress testing

### Phase 10: Deployment
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Monitoring and logging
