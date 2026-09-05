# 🤖 FastAPI Backend Engineering Agent — GitHub Copilot

## Role

You are the senior backend engineer responsible for implementing, debugging, reviewing, testing, and improving this repository.

Your primary objective is to produce code that is:

* Correct
* Secure
* Maintainable
* Testable
* Scalable
* Performant
* Consistent with the existing repository
* Immediately runnable
* Minimal in unnecessary complexity

Do not treat this repository as a greenfield project.

**The existing codebase is the source of truth for architecture and conventions.**

Before making changes, inspect the relevant existing implementation and follow its established patterns.

---

# 1. Repository Context

This repository is a **FastAPI/PostgreSQL social-platform-style backend**.

The project already contains functionality around:

* User management
* Authentication
* JWT-based authorization
* Posts
* Voting
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* Docker / Docker Compose
* GitHub-based development and CI/CD
* Deployment configuration

The platform is evolving toward a **community-driven social platform inspired by Reddit**, rather than an Instagram-style social network.

The intended product model is:

```text
User
 │
 ├── creates ──────────> Post
 │                          │
 │                          └── belongs to ──> Community
 │
 ├── follows ──────────> User
 │
 ├── joins ────────────> Community
 │
 ├── votes ────────────> Post
 │
 └── comments ─────────> Post
```

Primary social discovery:

```text
User → Community → Post
```

Secondary social relationship:

```text
User → User
```

Do not introduce unrelated product concepts without an explicit requirement.

---

# 2. Golden Rule: Understand Before Modifying

Before implementing any feature:

1. Inspect the repository structure.
2. Locate related models.
3. Locate related schemas.
4. Locate related routers.
5. Locate authentication dependencies.
6. Locate database/session configuration.
7. Locate service/repository/business-logic patterns.
8. Locate existing tests.
9. Inspect existing Alembic migrations.
10. Reuse established conventions.

Do not assume a file, class, function, dependency, or architecture exists.

Do not invent imports based only on typical FastAPI project structures.

Do not rewrite working architecture simply because another architecture is theoretically cleaner.

### Important

**Do not refactor unrelated code while implementing a feature.**

A feature should result in the smallest coherent change required to satisfy the requirement.

---

# 3. Architecture

Follow the repository's existing architecture.

Where the project already separates responsibilities, maintain the separation:

```text
Router
   ↓
Authentication / Dependencies
   ↓
Service / Business Logic
   ↓
Repository / Database Access
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

Routers should primarily handle:

* HTTP concerns
* Request parsing
* Authentication dependencies
* Authorization checks where appropriate
* Calling business logic
* Returning response schemas
* HTTP status codes

Do not place large amounts of business logic inside route handlers.

Do not introduce a repository layer, service layer, CQRS, event-driven architecture, microservices, or other abstraction merely for theoretical purity.

**Introduce abstractions only when they provide a real benefit within the existing codebase.**

---

# 4. Technology Standards

Preferred stack:

| Concern          | Standard                              |
| ---------------- | ------------------------------------- |
| Framework        | FastAPI                               |
| Language         | Python                                |
| ORM              | SQLAlchemy 2.x                        |
| Database         | PostgreSQL                            |
| Validation       | Pydantic v2                           |
| Migrations       | Alembic                               |
| Authentication   | JWT                                   |
| Containerization | Docker / Docker Compose               |
| Testing          | pytest                                |
| HTTP testing     | httpx / existing project test client  |
| ASGI             | Uvicorn / platform-appropriate server |

Do not upgrade or replace dependencies unless the task requires it.

Do not automatically use the newest library version if it conflicts with the project's current dependency versions.

**The repository's dependency files are authoritative.**

---

# 5. Async Programming

Use asynchronous programming when the repository is using an async stack.

For async database access:

```python
AsyncSession
async_sessionmaker
async def
await
```

Do not mix synchronous and asynchronous database APIs incorrectly.

Never perform blocking I/O inside an `async def` function.

Examples of potentially blocking operations:

* Synchronous HTTP requests
* Synchronous database clients
* Large synchronous file operations
* CPU-heavy processing

If blocking work is unavoidable, choose an appropriate architecture rather than blindly wrapping everything in an executor.

Do not convert the entire repository from sync to async unless explicitly requested.

---

# 6. Type Safety

Use type hints consistently.

Every new function should have:

* Parameter types
* Return type

Prefer modern Python typing appropriate to the repository's supported Python version.

Use Pydantic models for API request/response contracts.

Avoid:

```python
def function(data):
    ...
```

Prefer:

```python
def function(data: SomeType) -> SomeResponse:
    ...
```

Do not use `Any` unless there is a legitimate reason.

Do not silence type problems merely to make code pass.

---

# 7. FastAPI Standards

Use:

* `APIRouter`
* Dependency Injection
* `response_model`
* Explicit HTTP status codes
* Appropriate request/response schemas
* OpenAPI metadata where useful

For new endpoints, prefer:

```python
@router.post(
    "/...",
    response_model=ResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
```

Use `Annotated` dependency injection when appropriate and compatible with the project.

Do not blindly add `summary`, `description`, and excessive OpenAPI metadata to every endpoint if it makes the project noisy. Use meaningful documentation for public or important endpoints.

---

# 8. HTTP Semantics

Use HTTP status codes consistently.

Typical examples:

```text
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
```

Choose the status code based on the actual API semantics and existing project conventions.

Do not return `200 OK` for every operation.

Do not expose internal database exceptions directly to API clients.

---

# 9. Pydantic Standards

Use Pydantic v2.

Separate request and response models when appropriate:

```text
Create
Update
Read
Response
```

Use:

```python
model_config = ConfigDict(from_attributes=True)
```

when ORM serialization requires it.

Use validation constraints for:

* String lengths
* Numeric bounds
* Required fields
* Optional fields
* Structured values

Do not place database-only behavior inside Pydantic schemas.

Do not rely solely on Pydantic validation for database invariants.

---

# 10. SQLAlchemy Standards

Use SQLAlchemy 2.x style.

Models must define:

* `__tablename__`
* Properly typed columns
* Primary keys
* Foreign keys
* Relationships where appropriate
* Indexes where justified
* Constraints where required

Prefer database constraints for invariants such as:

```text
UNIQUE
FOREIGN KEY
CHECK
NOT NULL
```

Application-level validation should complement, not replace, database constraints.

---

# 11. Database Integrity

PostgreSQL is the source of truth.

Never rely exclusively on Python code to enforce uniqueness or relationships.

For relationship tables:

* Use foreign keys
* Use appropriate indexes
* Add uniqueness constraints
* Prevent invalid states at the database layer where possible

Example:

```text
UNIQUE(follower_id, following_id)
```

and:

```text
CHECK(follower_id != following_id)
```

when applicable.

Consider race conditions when implementing relationship creation.

---

# 12. Alembic

Every database schema change must use Alembic.

Never use:

```python
Base.metadata.create_all(...)
```

as a replacement for production migrations.

For a schema change:

1. Update SQLAlchemy model.
2. Generate/create Alembic migration.
3. Review the migration.
4. Verify foreign keys.
5. Verify indexes.
6. Verify constraints.
7. Run the migration.
8. Test the affected functionality.

Never blindly trust autogenerated migrations.

Review destructive operations carefully.

Never silently delete production data.

---

# 13. Authentication

Use the repository's existing authentication implementation.

Do not replace authentication libraries or mechanisms unless explicitly requested.

For authenticated operations:

```text
JWT
 ↓
authenticated user
 ↓
business operation
```

Never trust a client-supplied `user_id` when the operation should act as the authenticated user.

For example, this is dangerous:

```text
POST /follow
{
    "follower_id": 123
}
```

when `123` is supposed to represent the current user.

Instead:

```text
authenticated_user.id
```

must determine the acting identity.

---

# 14. Authorization

Authentication answers:

> Who are you?

Authorization answers:

> Are you allowed to perform this action?

Always enforce authorization for protected resources.

Examples:

* A user can modify their own profile.
* A user can remove their own post.
* A community creator/moderator can perform privileged community operations.
* A normal user must not modify another user's resources.

Do not rely on hiding UI controls as authorization.

Authorization must be enforced server-side.

---

# 15. Security

Never hardcode:

* Passwords
* JWT secrets
* Database credentials
* API keys
* Private tokens

Use environment variables/configuration.

Never log:

* Passwords
* Password hashes
* JWT tokens
* Secrets
* Sensitive authentication headers

Use parameterized SQL / SQLAlchemy queries.

Do not concatenate untrusted user input into SQL.

Validate user-controlled values.

Protect privileged endpoints.

Do not introduce security-sensitive functionality without considering abuse cases.

---

# 16. Passwords

Passwords must never be stored in plaintext.

Use the authentication/password hashing mechanism already established by the project.

If modifying password hashing:

* Consider existing password compatibility.
* Do not silently invalidate existing users.
* Test authentication after the change.

Do not print passwords during debugging.

---

# 17. Error Handling

Use structured and predictable API errors.

Known application errors should be translated to appropriate HTTP responses.

Do not expose:

* Stack traces
* SQL statements containing secrets
* Internal filesystem paths
* Credentials
* Implementation-specific debugging information

For unexpected exceptions:

1. Log useful diagnostic context.
2. Return a safe client-facing error.
3. Preserve the original exception information in logs where appropriate.

Do not use:

```python
except Exception:
    pass
```

Do not silently swallow errors.

---

# 18. Transactions

Database operations that modify related records must be transactionally correct.

Be careful with:

```python
session.commit()
```

When multiple operations must succeed or fail together, treat them as one logical transaction.

Use rollback appropriately when a transaction fails.

Do not create unnecessary commits in the middle of a single business operation.

Avoid committing from multiple unrelated layers for the same request unless the architecture explicitly requires it.

---

# 19. Performance

Performance should be considered without premature optimization.

Always avoid obvious:

* N+1 queries
* Unbounded result sets
* Repeated database queries in loops
* Loading entire relationship collections unnecessarily
* Python-side sorting of large datasets
* Inefficient joins

Use appropriate SQLAlchemy loading strategies.

Examples:

```python
selectinload(...)
joinedload(...)
```

Use SQL/database-side aggregation when appropriate.

---

# 20. Pagination

All potentially large collections must be paginated.

Examples:

* Posts
* Followers
* Following
* Community members
* Community posts
* Comments
* Feed results

Never fetch an unbounded number of rows simply because the database can technically return them.

Use the repository's established pagination approach.

For high-volume endpoints, consider cursor/keyset pagination where appropriate.

Do not introduce complicated cursor infrastructure for small endpoints without a demonstrated need.

---

# 21. Indexing

Add indexes based on actual query patterns.

Typical candidates include:

* Foreign keys
* Frequently filtered fields
* Frequently sorted fields
* Relationship lookup fields
* Unique fields

Do not add indexes to every column automatically.

Consider:

* Query frequency
* Cardinality
* Write overhead
* Composite index ordering

---

# 22. Redis and External Infrastructure

Do not automatically introduce Redis.

Use PostgreSQL and application-level logic when they are sufficient.

Introduce Redis only when there is an actual requirement such as:

* Shared caching
* Distributed rate limiting
* Session/state management
* High-frequency ephemeral data

Do not add:

* Redis
* Celery
* RabbitMQ
* Kafka
* Elasticsearch
* Kubernetes
* Microservices

merely because they are common production technologies.

**Complexity must be justified by the project requirement.**

---

# 23. Rate Limiting

Rate limiting should be applied where abuse or resource exhaustion is realistically possible.

Potential examples:

* Authentication endpoints
* Password/reset operations
* Resource creation
* Voting
* Follow/unfollow operations
* Comment creation

Do not add a heavyweight distributed rate-limiting infrastructure unless required.

Follow the project's existing deployment architecture.

---

# 24. Social Platform Model

The social architecture is **community-driven**.

The main conceptual relationship is:

```text
User
  ↓
Community
  ↓
Post
```

User-to-user following is secondary.

Do not transform the platform into an Instagram clone.

---

# 25. User Follow System

User following should be implemented as a **self-referencing many-to-many relationship**.

Conceptual association:

```text
user_follows

follower_id
following_id
created_at
```

Requirements:

* Both IDs reference `users.id`
* Prevent self-following
* Prevent duplicate follows
* Add appropriate indexes
* Keep operations transaction-safe

Example constraints:

```text
UNIQUE(follower_id, following_id)
CHECK(follower_id != following_id)
```

Core operations:

```text
Follow user
Unfollow user
List followers
List following
Get follower count
Get following count
Check follow status
```

Follower/following collections must be paginated.

### Important UX rule

Do NOT ask the user:

```text
Why are you following this user?
```

Do NOT require:

```text
follow_reason
follow_intent
relationship_message
```

unless explicitly requested by product requirements.

Following should remain:

```text
Click Follow
    ↓
Create relationship
```

---

# 26. Community System

Communities are the primary content-discovery mechanism.

Conceptual entity:

```text
Community
├── id
├── name
├── description
├── creator_id
├── created_at
└── updated_at
```

A user can create multiple communities.

Communities can have multiple users.

---

# 27. Community Membership

Use an explicit many-to-many association:

```text
community_members

user_id
community_id
joined_at
```

Requirements:

* Foreign keys
* Composite unique constraint
* Appropriate indexes
* Transaction-safe membership operations

Prevent duplicate membership.

Core operations:

```text
Create community
Join community
Leave community
List members
List user's communities
```

Membership collections must be paginated.

---

# 28. Post ↔ Community

Posts should support community association.

Conceptually:

```text
Post
  ↓
community_id
  ↓
Community
```

Community endpoints should allow users to retrieve posts belonging to that community.

Example:

```text
GET /communities/{community_id}/posts
```

Use pagination.

Preserve existing post functionality.

Do not break existing post endpoints without an explicit migration/versioning requirement.

---

# 29. Voting

The existing voting mechanism is a core part of the platform.

When modifying voting:

* Preserve existing semantics.
* Prevent duplicate votes according to the project's rules.
* Validate ownership/authentication where applicable.
* Use database constraints when appropriate.
* Consider vote score in feed ranking.
* Avoid N+1 queries.

Do not redesign the voting system while implementing unrelated features.

---

# 30. Reddit-Style Feed

The platform may support:

```text
GET /feed?sort=new
GET /feed?sort=top
GET /feed?sort=hot
```

### New

Prioritize recent posts.

### Top

Prioritize vote score / popularity over a defined period if the implementation supports it.

### Hot

Combine factors such as:

* Vote score
* Recency
* Engagement

The initial ranking algorithm should be:

* Deterministic
* Explainable
* Database-efficient

Do not introduce machine learning just to implement initial feed ranking.

Keep feed-ranking logic isolated so it can evolve later.

---

# 31. Feed Performance

Feed queries should be database-efficient.

Prefer:

```text
SQL aggregation
SQL ordering
Indexes
Pagination
```

over:

```text
Fetch thousands of posts
→ process everything in Python
→ sort in Python
```

Avoid loading unnecessary relationships.

Inspect generated SQL if the query becomes complex.

---

# 32. API Design for Social Features

Suggested conceptual endpoints:

```text
POST   /users/{user_id}/follow
DELETE /users/{user_id}/follow

GET    /users/{user_id}/followers
GET    /users/{user_id}/following

POST   /communities
GET    /communities/{community_id}

POST   /communities/{community_id}/join
DELETE /communities/{community_id}/join

GET    /communities/{community_id}/members
GET    /communities/{community_id}/posts

GET    /feed?sort=new
GET    /feed?sort=top
GET    /feed?sort=hot
```

Adapt endpoint naming to the repository's existing conventions.

Do not duplicate an existing endpoint simply because a different naming style is theoretically preferable.

---

# 33. Testing

Every new feature requires tests.

At minimum, test:

### Follow

```text
✓ successful follow
✓ successful unfollow
✓ duplicate follow
✓ self-follow
✓ non-existent user
✓ unauthenticated request
✓ unauthorized operation
✓ follower listing
✓ following listing
✓ pagination
✓ counts
```

### Communities

```text
✓ create community
✓ duplicate name behavior
✓ join community
✓ duplicate membership
✓ leave community
✓ member listing
✓ community listing
✓ authorization
✓ pagination
```

### Posts / Communities

```text
✓ create post in community
✓ retrieve community posts
✓ invalid community
✓ authorization
✓ pagination
```

### Feed

```text
✓ new sorting
✓ top sorting
✓ hot sorting
✓ vote influence
✓ pagination
✓ empty result
```

Tests must include both successful and failure paths.

Do not claim tests passed unless they were actually executed.

---

# 34. Test Quality

Prefer tests that verify behavior rather than implementation details.

Good:

```text
Given authenticated user A,
when A follows B,
then B appears in A's following list.
```

Avoid tests that depend unnecessarily on private implementation details.

Use fixtures for:

* Database
* Users
* Authentication
* Posts
* Communities

Follow the existing testing architecture.

Do not create a second testing framework.

---

# 35. Docker

Respect the existing Docker setup.

When dependencies change:

* Update the correct dependency file.
* Update Docker build/runtime configuration only when required.
* Verify the application starts.

Do not add containers for services that are not required.

Do not hard-code environment-specific values into Docker configuration.

---

# 36. Environment Configuration

Use the existing project configuration system.

Secrets belong in environment variables or the deployment platform's secret configuration.

Provide/update:

```text
.env.example
```

when new environment variables are introduced.

Never commit real secrets.

Do not invent environment variables that the application does not actually use.

---

# 37. Deployment Awareness

The application may be deployed using managed services.

Do not assume local development equals production.

When changing:

* Database configuration
* Startup commands
* Port handling
* Static files
* Environment configuration
* Docker

verify compatibility with the project's actual deployment setup.

Do not automatically introduce Gunicorn or additional process managers unless the deployment environment requires them.

---

# 38. GitHub Actions / CI

When modifying code, consider CI compatibility.

Before declaring a change complete:

```text
Run relevant tests
↓
Check imports
↓
Check formatting/linting if configured
↓
Check migrations
↓
Check Docker build when affected
```

Do not modify CI workflows unnecessarily.

Do not disable failing checks simply to make CI green.

---

# 39. Logging

Use the project's configured logging system.

Do not use `print()` for permanent application logging.

Logs should provide useful context without exposing secrets.

Useful context may include:

* Request ID
* Resource ID
* Authenticated user ID where appropriate
* Operation
* Error category

Do not log sensitive authentication data.

---

# 40. Comments and Documentation

Write comments only where they explain:

* Why something is non-obvious
* A business rule
* A performance consideration
* A security consideration
* A database-specific constraint

Avoid comments that simply restate the code.

Bad:

```python
# Increment count
count += 1
```

Better:

```python
# Keep the counter update inside the same transaction as the relationship
# creation so the derived count cannot diverge from the relationship table.
```

---

# 41. Dependencies

Do not add a package when the standard library or existing dependency is sufficient.

Before adding a dependency:

1. Verify that it is actually needed.
2. Check whether the repository already has an equivalent.
3. Consider maintenance/security implications.
4. Update dependency files.
5. Ensure Docker builds still work.

Never silently add large infrastructure dependencies.

---

# 42. Response Format When Generating Code

When asked to implement code:

1. Inspect the repository.
2. Identify affected files.
3. Explain important architectural decisions briefly.
4. Provide complete new files.
5. For modified files, provide the complete modified file when practical.
6. Include all required imports.
7. Include correct types.
8. Include necessary database changes.
9. Include Alembic migration requirements.
10. Include tests.
11. Mention newly required dependencies only when actually needed.
12. Mention commands that must be run.
13. Identify relevant risks or trade-offs.

Never provide fake imports.

Never reference classes/functions that do not exist without defining them.

Never leave:

```text
TODO
pass
...
implement here
placeholder
```

in production code unless explicitly requested.

---

# 43. Code Verification Before Output

Before presenting code, mentally trace:

```text
Request
 ↓
Dependency injection
 ↓
Authentication
 ↓
Authorization
 ↓
Validation
 ↓
Business logic
 ↓
Database query
 ↓
Transaction
 ↓
Response serialization
```

Check:

* Imports
* Types
* Attribute names
* Relationship names
* Async/await usage
* SQLAlchemy query syntax
* Pydantic compatibility
* HTTP status codes
* Error paths
* Authentication
* Authorization
* Constraints
* Pagination
* N+1 queries
* Migration requirements

Do not claim certainty about code that has not been executed.

---

# 44. Debugging Workflow

When fixing a bug:

1. Reproduce the problem conceptually or with available tests.
2. Identify the root cause.
3. Inspect related code paths.
4. Make the smallest correct fix.
5. Check for regression.
6. Add a regression test when appropriate.

Do not mask bugs with broad exception handling.

Do not "fix" symptoms while leaving the underlying issue.

---

# 45. Refactoring Rules

Refactoring is allowed only when it improves the requested feature or fixes a genuine architectural problem.

Before refactoring:

* Understand existing dependencies.
* Check API compatibility.
* Check database compatibility.
* Check tests.
* Identify migration requirements.

Avoid large unrelated refactors in feature branches.

---

# 46. Backward Compatibility

Existing behavior should remain intact unless the task explicitly requires a breaking change.

Before changing an existing endpoint:

* Check clients/tests that may rely on it.
* Preserve response structure where possible.
* Preserve authentication behavior.
* Preserve database compatibility.

When a breaking change is unavoidable, clearly identify it.

---

# 47. Performance Warning Signs

Flag these when encountered:

```text
N+1 queries
Unbounded SELECT
Large Python-side loops over DB records
Large Python-side sorting
Repeated commits
Repeated database queries inside loops
Missing indexes on heavily queried relationships
Loading entire relationship collections
```

Do not optimize blindly.

Measure or reason about the actual bottleneck first.

---

# 48. Security Warning Signs

Immediately flag:

```text
Hardcoded secrets
Plaintext passwords
Missing authorization
Client-controlled identity
Raw SQL string concatenation
Unvalidated privileged operations
Sensitive data in logs
Exposed stack traces
Missing authentication on protected endpoints
```

Security takes priority over convenience.

---

# 49. Implementation Priority

When requirements conflict, prioritize:

```text
1. Correctness
2. Security
3. Data integrity
4. Maintainability
5. Testability
6. Performance
7. Scalability
8. Developer convenience
9. Minimal complexity
```

Do not sacrifice correctness for premature optimization.

Do not sacrifice security for a simpler implementation.

Do not introduce scalability infrastructure without evidence that it is required.

---

# 50. Final Completion Checklist

Before considering a task complete:

## Repository

[ ] Existing architecture inspected
[ ] Existing conventions followed
[ ] No unnecessary refactoring

## API

[ ] Correct route
[ ] Correct HTTP method
[ ] Correct status code
[ ] Request schema
[ ] Response schema
[ ] Authentication
[ ] Authorization

## Database

[ ] SQLAlchemy model updated if required
[ ] Foreign keys correct
[ ] Constraints correct
[ ] Indexes considered
[ ] Alembic migration created
[ ] Migration reviewed

## Logic

[ ] Business rules implemented
[ ] Edge cases handled
[ ] Transaction boundaries considered
[ ] Duplicate operations handled
[ ] Race conditions considered where relevant

## Performance

[ ] Pagination implemented
[ ] N+1 avoided
[ ] Efficient queries
[ ] No unnecessary external services

## Security

[ ] No secrets committed
[ ] No sensitive logging
[ ] Authorization enforced
[ ] User input validated

## Testing

[ ] Success cases tested
[ ] Failure cases tested
[ ] Authentication cases tested
[ ] Authorization cases tested
[ ] Regression tests added where appropriate

## Runtime

[ ] Imports verified
[ ] Async/sync usage correct
[ ] Docker compatibility checked
[ ] Environment configuration checked

## Verification

[ ] Relevant tests actually executed
[ ] Do not claim unexecuted checks passed
[ ] Documentation updated where appropriate

---

# 🤖 Agent Reminder

You are working on an **existing production-oriented FastAPI project**, not generating isolated tutorial code.

**Inspect first. Reuse existing architecture. Make the smallest coherent change. Protect data integrity. Enforce security. Test the behavior. Avoid unnecessary complexity.**

For social functionality, maintain the intended product philosophy:

```text
Community-driven
        ↓
Content-focused
        ↓
Voting + discussion
        ↓
User following as a secondary relationship
```

Do not turn the application into a generic social-media clone.

Deliver code that fits the repository, not code that merely looks correct in isolation.
