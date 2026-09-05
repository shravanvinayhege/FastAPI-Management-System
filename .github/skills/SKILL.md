---

name: fastapi-social-platform
description: Extend and maintain this FastAPI PostgreSQL social platform safely. Use when implementing or modifying users, authentication, posts, voting, followers/following, communities, feeds, comments, APIs, SQLAlchemy models, Pydantic schemas, Alembic migrations, tests, Docker, or related backend functionality.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# FastAPI Social Platform Engineering Skill

## 1. Project Context

This repository is a FastAPI-based social platform backed by PostgreSQL.

Existing technology direction:

* Python
* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Pydantic v2
* JWT authentication
* Alembic migrations
* Docker / Docker Compose
* Render deployment
* OpenAPI / Swagger / ReDoc

The repository already contains users, posts, voting, authentication, CRUD functionality, database migrations, and API routers.

Before changing code:

1. Inspect the existing project structure.
2. Identify the existing model, schema, router, dependency, database-session, authentication, and migration patterns.
3. Reuse existing abstractions instead of creating parallel implementations.
4. Do not rewrite working functionality unnecessarily.
5. Maintain backward compatibility unless the task explicitly requires a breaking change.

---

# 2. Architecture Rules

Follow the repository's existing separation of concerns.

Preferred flow:

HTTP Request
→ Router
→ Authentication / dependencies
→ Service or business logic
→ SQLAlchemy / database access
→ PostgreSQL
→ Pydantic response schema

Do not place substantial business logic directly inside route handlers.

Routers should primarily:

* Validate request inputs
* Resolve authenticated user
* Call business logic
* Return response schemas
* Map expected exceptions to HTTP responses

Business rules should live outside routers when the existing architecture provides an appropriate service/repository layer.

Do not duplicate database queries across multiple routers when the logic can be reused.

---

# 3. Database Rules

Use PostgreSQL as the source of truth.

For every schema change:

1. Modify SQLAlchemy models.
2. Create an Alembic migration.
3. Review the generated migration manually.
4. Ensure foreign keys are correct.
5. Add appropriate indexes.
6. Add uniqueness constraints for relationship tables where necessary.
7. Consider delete/update behavior explicitly.
8. Test upgrade and downgrade paths.

Never modify production schema manually as a substitute for an Alembic migration.

Avoid storing derived counters unless there is a clear performance requirement.

When counters are stored, define how they remain consistent with transactional updates.

---

# 4. SQLAlchemy Relationship Rules

Use explicit relationship definitions for self-referencing and many-to-many relationships.

For user-to-user relationships, prefer an association table/model rather than adding JSON arrays or comma-separated IDs.

Example conceptual relationship:

User
→ follower relationships
→ following relationships
→ User

Always prevent:

* Self-following
* Duplicate relationships
* Invalid foreign keys

Use database constraints in addition to application-level validation.

Do not rely only on Python checks for uniqueness or race-sensitive rules.

---

# 5. Authentication and Authorization

Use the repository's existing JWT authentication mechanism.

For authenticated operations:

* Derive the acting user from the authenticated token/dependency.
* Never trust a `user_id` supplied by the client when it represents the current authenticated user.
* Verify resource ownership before update/delete operations.
* Do not expose privileged operations through unauthenticated routes.

Never log:

* JWT tokens
* Passwords
* Password hashes
* Secrets
* Database credentials

Never commit secrets to source control.

---

# 6. API Design

Follow REST-oriented resource naming consistent with the existing API.

Prefer:

POST   /users/{id}/follow
DELETE /users/{id}/follow

GET    /users/{id}/followers
GET    /users/{id}/following

POST   /communities
POST   /communities/{id}/join
DELETE /communities/{id}/join

GET    /communities/{id}/posts

GET    /feed?sort=new
GET    /feed?sort=top
GET    /feed?sort=hot

Do not introduce unnecessary endpoints when an existing endpoint can naturally support the feature.

Use appropriate HTTP status codes.

Examples:

* 200 for successful retrieval/update
* 201 for resource creation
* 204 where an empty successful response is appropriate
* 400 for invalid requests
* 401 for unauthenticated requests
* 403 for authenticated but unauthorized requests
* 404 for missing resources
* 409 for genuine resource conflicts such as duplicate relationships

Use Pydantic v2 schemas for request and response validation.

Do not expose raw SQLAlchemy model objects as the public API contract when a response schema exists.

---

# 7. Reddit-Inspired Social Model

The platform should be community-driven rather than an Instagram-style follower clone.

Primary relationship:

User
→ Community
→ Post

Secondary relationship:

User
→ User

The user-to-user follow interaction must remain simple.

Do NOT ask the user for a reason when following another user.

Follow should be:

Follow
→ create relationship

not:

Follow
→ ask for intent/reason
→ create relationship

---

# 8. Follow System

Implement user-to-user following as a self-referencing many-to-many association.

Recommended conceptual table:

user_follows

* follower_id
* following_id
* created_at

Requirements:

* Foreign key to users for both IDs
* Composite unique constraint on follower_id + following_id
* Constraint preventing follower_id == following_id
* Index follower_id
* Index following_id
* Transaction-safe creation/removal

Expose:

* Follow
* Unfollow
* List followers
* List following
* Follower count
* Following count
* Follow status for the authenticated user

Pagination is required for follower/following lists.

Do not load an entire follower/following collection into memory.

---

# 9. Community System

Communities are the main social grouping.

A community should contain conceptually:

* id
* name
* description
* creator_id
* created_at
* updated_at

A community can have many users.

Users can join or leave communities.

Membership should use an explicit many-to-many association:

community_members

* user_id
* community_id
* joined_at

Requirements:

* Composite unique constraint
* Foreign keys
* Appropriate indexes
* Pagination for members
* Authorization for community-management operations

Community names should have appropriate uniqueness behavior.

Do not use case-sensitive duplicate names such as:

Python
python
PYTHON

unless the product requirements explicitly permit this.

---

# 10. Post and Community Integration

Posts should support association with a community.

Conceptually:

Post
→ community_id
→ Community

Community endpoints should support retrieving posts belonging to that community.

Use pagination.

Apply authorization rules consistently when creating, editing, or deleting posts.

Do not break existing post endpoints merely to introduce communities.

---

# 11. Voting

The existing voting mechanism must remain compatible with new functionality.

When implementing feeds or rankings:

* Use vote score rather than blindly counting rows when possible.
* Avoid N+1 queries.
* Prefer database-side aggregation.
* Preserve the rule that a user should have the intended number/type of votes according to the existing model.
* Do not silently change existing voting semantics.

When modifying voting queries, add regression tests.

---

# 12. Feed Design

The platform should eventually support Reddit-style sorting.

Required conceptual modes:

* new
* top
* hot

Initial implementation should be deterministic and explainable.

Do not introduce machine learning merely to rank posts.

A reasonable initial ranking can use:

* vote score
* creation time
* engagement
* community/user relevance

Keep ranking logic isolated so it can evolve independently.

Avoid expensive Python-side sorting of large datasets.

Prefer SQL/database-side ordering and aggregation.

Use indexes to support feed queries.

---

# 13. Pagination

Any potentially unbounded collection must be paginated.

Examples:

* followers
* following
* community members
* community posts
* feed
* comments
* votes if exposed

Prefer the repository's existing pagination pattern.

Do not fetch thousands of database rows and slice them in Python.

For high-volume endpoints, consider keyset/cursor pagination instead of deep OFFSET pagination.

---

# 14. Query Performance

Avoid N+1 query patterns.

Before adding a query:

* Determine whether relationships can be eagerly loaded.
* Check whether aggregation can happen in SQL.
* Check whether an index is needed.
* Avoid repeated queries inside loops.

For feed/community/follower endpoints, inspect the generated SQL when performance is uncertain.

Do not prematurely add Redis, Celery, Elasticsearch, or other infrastructure unless the repository requirements justify it.

Keep the first implementation PostgreSQL-centric and simple.

---

# 15. Validation

Validation should happen at multiple appropriate layers.

Pydantic:

* request shape
* required/optional fields
* basic constraints

Application logic:

* business rules
* authorization
* state transitions

PostgreSQL:

* referential integrity
* uniqueness
* invariant constraints

Never depend on only one layer for critical invariants.

---

# 16. Error Handling

Return predictable API errors.

Do not expose raw database exceptions to clients.

Translate known constraint violations into meaningful HTTP responses.

Examples:

* Duplicate follow → 409 or the repository's established idempotent behavior
* Self-follow → 400
* Missing user → 404
* Unauthorized modification → 403
* Unauthenticated request → 401

Match existing project conventions before introducing new error formats.

---

# 17. Testing Requirements

Every new feature must include tests.

For the follow system test:

* successful follow
* duplicate follow
* self-follow
* unfollow
* non-existent user
* unauthorized request
* follower list
* following list
* pagination
* counts

For communities test:

* create community
* duplicate community-name behavior
* join
* duplicate membership
* leave
* post in community
* community post retrieval
* authorization
* pagination

For feeds test:

* new ordering
* top ordering
* hot ordering
* voting influence
* pagination
* empty feed
* authorization where applicable

Test both happy paths and failure paths.

---

# 18. Alembic Migration Rules

Never skip migrations for model changes.

Use migration naming that describes the change.

Before finalizing a migration:

* Inspect generated SQL/operations.
* Confirm foreign keys.
* Confirm indexes.
* Confirm constraints.
* Confirm nullable/non-nullable behavior.
* Test upgrade.
* Test downgrade where practical.

Avoid destructive migrations unless explicitly required.

Do not silently delete existing production data.

---

# 19. Code Quality

Prefer:

* type hints
* small functions
* descriptive names
* explicit business rules
* reusable dependencies
* clear Pydantic schemas
* predictable exception handling

Avoid:

* giant route functions
* hidden global state
* duplicated SQL
* magic numbers
* unnecessary abstraction
* premature microservices
* unnecessary dependencies

Do not refactor unrelated code while implementing a feature unless the refactor is necessary for correctness.

---

# 20. Docker and Deployment

Respect the existing Docker and Docker Compose configuration.

Do not introduce a new deployment architecture unnecessarily.

When adding dependencies:

* update requirements appropriately
* verify Docker build
* verify application startup
* verify environment-variable handling

Never hard-code database credentials, JWT secrets, or deployment secrets.

Remember that deployment environments may differ from local development.

---

# 21. GitHub Actions / CI

Before declaring a task complete:

1. Run relevant tests.
2. Run lint/type checks if configured.
3. Verify imports.
4. Verify Alembic migration state.
5. Verify Docker build if the change affects deployment/runtime dependencies.
6. Check that existing tests still pass.

Do not claim a test passed unless it was actually executed.

Do not ignore failing CI without explaining the failure and its cause.

---

# 22. Implementation Workflow

For every feature, follow:

1. Inspect repository architecture.
2. Identify affected models.
3. Identify affected schemas.
4. Identify affected services/repositories.
5. Identify affected routers.
6. Design database changes.
7. Implement model changes.
8. Create Alembic migration.
9. Implement business logic.
10. Implement API endpoints.
11. Add validation and authorization.
12. Add tests.
13. Run tests.
14. Check migration behavior.
15. Check Docker/runtime compatibility.
16. Review for N+1 queries and security issues.
17. Update API documentation/README when appropriate.

Do not skip directly from requirement to code without examining the existing implementation.

---

# 23. Change Scope

When asked to implement a feature:

* Make the smallest coherent change.
* Preserve existing API behavior.
* Avoid unrelated refactoring.
* Reuse existing conventions.
* Do not rename existing tables/endpoints/classes unless necessary.
* Do not replace working infrastructure with a new framework.

If the requested implementation conflicts with existing architecture, adapt the feature to the architecture before introducing a new pattern.

---

# 24. Final Verification Checklist

Before completing any task, verify:

[ ] Existing functionality remains intact
[ ] SQLAlchemy relationships are correct
[ ] Alembic migration exists
[ ] Constraints/indexes are present
[ ] Authentication is enforced where required
[ ] Authorization is correct
[ ] Pydantic schemas are used
[ ] Pagination is implemented for collections
[ ] N+1 queries are avoided
[ ] Tests cover success and failure cases
[ ] Docker/runtime compatibility is preserved
[ ] No secrets are committed
[ ] No unnecessary dependencies were added
[ ] Relevant tests were actually executed
[ ] README/API documentation is updated when needed

When uncertain, inspect the existing code and follow its established patterns instead of inventing a new architecture.
