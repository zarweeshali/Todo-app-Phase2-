# Unified Specification: Hackathon Todo – Phase II (Full-Stack Web Application)

**Document Type**: Unified Feature Specification  
**Created**: 2026-02-08  
**Version**: 2.0 (Comprehensive)  
**Status**: FINAL  
**Spec-Kit Compatibility**: Yes

---

## Executive Summary

Phase II transforms the console-based Todo application into a secure, multi-user full-stack web application. This unified specification defines all requirements for authentication, task management, API design, database schema, and frontend implementation.

**Key Characteristics**:
- ✅ Multi-user support with JWT-based authentication
- ✅ Secure REST API with stateless backend
- ✅ Persistent storage via Neon PostgreSQL
- ✅ Responsive Next.js frontend
- ✅ Spec-driven, agent-implemented development

---

## Part 1: Authentication System

### 1.1 Overview

Users authenticate via Better Auth on the frontend. Upon successful login, Better Auth issues a JWT token containing the user's identity. This token is attached to all API requests and verified by the backend.

### 1.2 Authentication Flow

```
1. User signs up or logs in via Better Auth
   └─> Better Auth validates credentials
   
2. Better Auth issues JWT token
   └─> Token contains user_id in "sub" claim
   └─> Token expires in 24 hours
   
3. Frontend stores JWT (secure storage)
   └─> localStorage or sessionStorage
   
4. Frontend attaches token to API requests
   └─> Authorization: Bearer {jwt_token}
   
5. Backend receives request
   └─> Extracts JWT from header
   └─> Verifies signature with shared secret
   └─> Validates expiration
   └─> Extracts user_id from "sub" claim
   
6. Request processed with authenticated user_id
   └─> User_id used to filter/own resources
```

### 1.3 User Sign-Up

**Flow**:
1. User navigates to signup page
2. Enters email, password, name
3. Better Auth validates & creates user
4. User redirected to login
5. User logs in with credentials

**User Data Stored**:
- Email (unique)
- Password hash (via Better Auth)
- Name (optional)
- Created at (timestamp)
- Updated at (timestamp)

### 1.4 User Sign-In

**Flow**:
1. User navigates to login page
2. Enters email & password
3. Better Auth validates credentials
4. JWT token issued on success
5. Frontend stores token
6. User redirected to dashboard

**JWT Token Structure**:
```json
{
  "sub": "user-uuid-string",
  "email": "user@example.com",
  "exp": 1707359345,
  "iat": 1707272945
}
```

### 1.5 Token Management

**Token Verification**:
- Backend uses shared SECRET_KEY to verify JWT
- Signature validation on every request
- Expiration check (404 hours)
- Invalid token → 401 Unauthorized

**Token Refresh**:
- Tokens expire after 24 hours
- Frontend may implement refresh token logic
- On 401, user redirected to login

**Token Revocation**:
- No server-side token blacklist (stateless design)
- Token valid until expiration
- User logout clears token from frontend storage

### 1.6 Security Requirements

- ✅ Passwords hashed by Better Auth
- ✅ HTTPS in production (TLS 1.2+)
- ✅ JWT verified on every request
- ✅ Token never logged or exposed
- ✅ No user identity from request body

---

## Part 2: Task Management (CRUD)

### 2.1 Task Entity

**Properties**:
```
Task {
  id:          UUID (primary key)
  user_id:     UUID (foreign key → users)
  title:       String (1-500 chars, required)
  description: String (0-2000 chars, optional)
  completed:   Boolean (default: false)
  created_at:  DateTime (auto-set)
  updated_at:  DateTime (auto-updated)
}
```

### 2.2 Create Task

**User Story**: Users can create a new task to add to their list

**Endpoint**: `POST /api/{user_id}/tasks`

**Request**:
```http
POST /api/12345678-1234-5678-1234-567812345678/tasks
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, cheese"
}
```

**Request Validation**:
- `title`: Required, 1-500 characters, non-empty string
- `description`: Optional, 0-2000 characters
- `user_id` in URL: Must match JWT user_id (backend enforces)

**Response (201 Created)**:
```json
{
  "id": "87654321-4321-8765-4321-876543218765",
  "user_id": "12345678-1234-5678-1234-567812345678",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, cheese",
  "completed": false,
  "created_at": "2026-02-08T14:30:00Z",
  "updated_at": "2026-02-08T14:30:00Z"
}
```

**Error Responses**:
- 401 Unauthorized: Missing or invalid JWT
- 400 Bad Request: URL user_id doesn't match JWT user_id
- 422 Unprocessable Entity: Invalid input (missing title, etc.)

### 2.3 Read Tasks

**User Story**: Users can view all their tasks

**Endpoint**: `GET /api/{user_id}/tasks`

**Request**:
```http
GET /api/12345678-1234-5678-1234-567812345678/tasks
Authorization: Bearer {jwt_token}
```

**Query Parameters** (optional):
- `status`: Filter by "all" (default), "completed", or "pending"
- `limit`: Max results (default: 100, max: 1000)
- `offset`: Pagination offset (default: 0)

**Response (200 OK)**:
```json
[
  {
    "id": "87654321-4321-8765-4321-876543218765",
    "user_id": "12345678-1234-5678-1234-567812345678",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, cheese",
    "completed": false,
    "created_at": "2026-02-08T14:30:00Z",
    "updated_at": "2026-02-08T14:30:00Z"
  },
  {
    "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "user_id": "12345678-1234-5678-1234-567812345678",
    "title": "Call mom",
    "description": null,
    "completed": true,
    "created_at": "2026-02-07T10:00:00Z",
    "updated_at": "2026-02-08T12:00:00Z"
  }
]
```

**Error Responses**:
- 401 Unauthorized: Missing or invalid JWT
- 400 Bad Request: URL user_id doesn't match JWT user_id

### 2.4 Read Single Task

**User Story**: Users can view details of a specific task

**Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Request**:
```http
GET /api/12345678-1234-5678-1234-567812345678/tasks/87654321-4321-8765-4321-876543218765
Authorization: Bearer {jwt_token}
```

**Response (200 OK)**:
```json
{
  "id": "87654321-4321-8765-4321-876543218765",
  "user_id": "12345678-1234-5678-1234-567812345678",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, cheese",
  "completed": false,
  "created_at": "2026-02-08T14:30:00Z",
  "updated_at": "2026-02-08T14:30:00Z"
}
```

**Error Responses**:
- 401 Unauthorized: Missing or invalid JWT
- 400 Bad Request: URL user_id doesn't match JWT user_id
- 404 Not Found: Task doesn't exist or belongs to different user

### 2.5 Update Task

**User Story**: Users can edit task title, description, and completion status

**Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Request**:
```http
PUT /api/12345678-1234-5678-1234-567812345678/tasks/87654321-4321-8765-4321-876543218765
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, cheese, vegetables",
  "completed": false
}
```

**Update Rules**:
- Partial updates allowed (only update provided fields)
- Title: 1-500 characters (if provided)
- Description: 0-2000 characters (if provided)
- Completed: Boolean (if provided)
- Updated_at automatically set to current time

**Response (200 OK)**:
```json
{
  "id": "87654321-4321-8765-4321-876543218765",
  "user_id": "12345678-1234-5678-1234-567812345678",
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, cheese, vegetables",
  "completed": false,
  "created_at": "2026-02-08T14:30:00Z",
  "updated_at": "2026-02-08T15:00:00Z"
}
```

**Error Responses**:
- 401 Unauthorized: Missing or invalid JWT
- 400 Bad Request: URL user_id doesn't match JWT user_id
- 404 Not Found: Task doesn't exist or belongs to different user
- 422 Unprocessable Entity: Invalid input (title empty, etc.)

### 2.6 Delete Task

**User Story**: Users can delete a task

**Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Request**:
```http
DELETE /api/12345678-1234-5678-1234-567812345678/tasks/87654321-4321-8765-4321-876543218765
Authorization: Bearer {jwt_token}
```

**Response (204 No Content)**:
```
(empty body)
```

**Error Responses**:
- 401 Unauthorized: Missing or invalid JWT
- 400 Bad Request: URL user_id doesn't match JWT user_id
- 404 Not Found: Task doesn't exist or belongs to different user

### 2.7 Toggle Task Completion

**User Story**: Users can quickly mark tasks as complete/incomplete

**Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Request**:
```http
PATCH /api/12345678-1234-5678-1234-567812345678/tasks/87654321-4321-8765-4321-876543218765/complete
Authorization: Bearer {jwt_token}

{
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "id": "87654321-4321-8765-4321-876543218765",
  "user_id": "12345678-1234-5678-1234-567812345678",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, cheese",
  "completed": true,
  "created_at": "2026-02-08T14:30:00Z",
  "updated_at": "2026-02-08T15:05:00Z"
}
```

---

## Part 3: Authorization & Security

### 3.1 Authorization Rules

**Every API endpoint must enforce**:

1. ✅ JWT token is present in Authorization header
2. ✅ JWT token is valid and not expired
3. ✅ JWT signature verified using SECRET_KEY
4. ✅ User_id extracted from JWT "sub" claim
5. ✅ User_id in URL matches JWT user_id
6. ✅ Task belongs to authenticated user
7. ✅ Return 404 if resource unauthorized (no data leakage)

### 3.2 User Isolation

**Requirements**:
- User A cannot see User B's tasks
- User A cannot modify User B's tasks
- User A cannot delete User B's tasks
- User A cannot get User B's task by ID
- Cross-user access attempt → 404 Not Found

**Database Enforcement**:
- Foreign key: tasks.user_id references users.id
- Every query filters by user_id from JWT

**API Enforcement**:
- URL user_id checked against JWT user_id
- Task ownership verified before operation
- 404 returned for unauthorized access

### 3.3 Security Implementation

**JWT Verification**:
```python
# Backend extracts and verifies JWT
1. Get token from "Authorization: Bearer {token}"
2. Decode token using SECRET_KEY
3. Verify signature
4. Check expiration
5. Extract user_id from "sub" claim
6. Use user_id for all operations
```

**User Identity Trust**:
- ✅ Trust only JWT claims (verified signature)
- ✅ Ignore user_id from request body
- ✅ Ignore user_id from cookies or other sources
- ✅ URL user_id must match JWT user_id

**Error Handling**:
- Invalid token → 401 Unauthorized
- Expired token → 401 Unauthorized
- Malformed header → 401 Unauthorized
- User mismatch → 400 Bad Request
- Resource unauthorized → 404 Not Found

---

## Part 4: API Design & Specifications

### 4.1 Base URL

```
http://localhost:8000/api    (Development)
https://api.yourdomain.com   (Production)
```

### 4.2 Endpoints Summary

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/api/{user_id}/tasks` | ✅ | Create task |
| GET | `/api/{user_id}/tasks` | ✅ | List tasks |
| GET | `/api/{user_id}/tasks/{id}` | ✅ | Get task |
| PUT | `/api/{user_id}/tasks/{id}` | ✅ | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | ✅ | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | ✅ | Toggle completion |

### 4.3 HTTP Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful read/update |
| 201 | Created | Task successfully created |
| 204 | No Content | Successful delete |
| 400 | Bad Request | URL user_id doesn't match JWT |
| 401 | Unauthorized | Missing/invalid JWT token |
| 404 | Not Found | Resource doesn't exist or unauthorized |
| 422 | Unprocessable Entity | Validation error (bad input) |
| 500 | Internal Server Error | Server error |

### 4.4 Error Response Format

```json
{
  "detail": "Error message explaining what went wrong"
}
```

**Examples**:
```json
{ "detail": "Invalid token" }
{ "detail": "Task not found" }
{ "detail": "Title must be between 1 and 500 characters" }
```

### 4.5 CORS Configuration

**Allowed Origins**:
- `http://localhost:3000` (development frontend)
- `http://localhost:5173` (Vite dev server)
- `https://yourdomain.com` (production frontend)

**Allowed Methods**: GET, POST, PUT, DELETE, PATCH, OPTIONS

**Allowed Headers**: Content-Type, Authorization

**Credentials**: Allowed (for cookies if needed)

---

## Part 5: Database Schema

### 5.1 Users Table

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  password_hash VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_users_email ON email
);
```

**Fields**:
- `id`: Unique identifier (UUID)
- `email`: User's email (unique)
- `name`: User's display name
- `password_hash`: Hashed password (via Better Auth)
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### 5.2 Tasks Table

```sql
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(500) NOT NULL,
  description VARCHAR(2000),
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_tasks_user_id ON user_id,
  INDEX idx_tasks_user_completed ON (user_id, completed)
);
```

**Fields**:
- `id`: Unique identifier (UUID)
- `user_id`: Foreign key to users (cascade delete)
- `title`: Task title (1-500 chars, required)
- `description`: Task description (0-2000 chars, optional)
- `completed`: Completion status (default: false)
- `created_at`: Task creation timestamp
- `updated_at`: Last update timestamp

**Constraints**:
- ✅ Foreign key constraint on user_id
- ✅ Cascade delete (deleting user deletes tasks)
- ✅ Index on user_id (query optimization)
- ✅ Index on (user_id, completed) (filter optimization)

### 5.3 Database Provider

**Neon Serverless PostgreSQL**:
- Managed database (no setup required)
- Automatic backups
- SSL connections by default
- Connection pooling built-in
- Scalable to production

**Connection String Format**:
```
postgresql+asyncpg://user:password@host/dbname
```

---

## Part 6: Frontend Specifications

### 6.1 Technology Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth
- **State Management**: React hooks (useState, useEffect)
- **HTTP Client**: Fetch API with JWT injection

### 6.2 Page Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Landing/auth page
│   ├── dashboard/
│   │   └── page.tsx         # Task list (protected)
│   └── globals.css          # Tailwind imports
├── components/
│   ├── LoginForm.tsx        # Better Auth login
│   ├── SignupForm.tsx       # Better Auth signup
│   ├── TaskList.tsx         # Task list display
│   ├── TaskForm.tsx         # Create/edit task
│   ├── TaskItem.tsx         # Individual task
│   └── Header.tsx           # Navigation
├── lib/
│   └── api.ts               # API client with JWT
├── types/
│   └── index.ts             # TypeScript types
└── styles/
    └── globals.css          # Global styles
```

### 6.3 Authentication UI

**Login Page**:
- Email input field
- Password input field
- Login button
- Sign up link
- Error message display
- Loading state

**Sign Up Page**:
- Email input field
- Password input field
- Name input field
- Sign up button
- Login link
- Error message display
- Password validation feedback

### 6.4 Task Management UI

**Task List View**:
- Display all user's tasks
- Show task title, description (if any), completion status
- Filter buttons: All / Completed / Pending
- Create task button
- Sort options (newest/oldest)
- Empty state message
- Loading state

**Create Task Form**:
- Title input (required)
- Description textarea (optional)
- Create button
- Cancel button
- Form validation
- Error messages

**Task Item**:
- Task title
- Task description
- Completion checkbox
- Edit button
- Delete button
- Edit/delete confirmation
- Loading state

**Edit Task Form**:
- Edit mode for task
- Update title & description
- Save button
- Cancel button
- Delete option
- Validation feedback

### 6.5 API Client Integration

**JWT Injection**:
```typescript
// Every API call automatically includes JWT
Authorization: Bearer {token_from_better_auth}
```

**Error Handling**:
- 401 errors → redirect to login
- 404 errors → show "task not found"
- 422 errors → show validation errors
- 500 errors → show "server error"

**Loading States**:
- Show spinner during API calls
- Disable buttons while loading
- Prevent duplicate submissions

### 6.6 Responsive Design

**Mobile (< 768px)**:
- Single column layout
- Full-width buttons
- Optimized touch targets
- Vertical scrolling

**Tablet (768px - 1024px)**:
- Two-column layout option
- Balanced spacing
- Medium text sizes

**Desktop (> 1024px)**:
- Multi-column layout option
- Sidebar navigation option
- Larger interactive areas

---

## Part 7: Backend Specifications

### 7.1 Technology Stack

- **Framework**: FastAPI 0.104+
- **Language**: Python 3.8+
- **ORM**: SQLModel
- **Database Driver**: SQLAlchemy (async)
- **Authentication**: JWT (HS256)

### 7.2 Application Structure

```
backend/
├── main.py                 # FastAPI app initialization
├── auth.py                 # JWT verification
├── models.py               # SQLModel definitions
├── db.py                   # Database connection
├── routes/
│   ├── __init__.py
│   └── tasks.py            # Task endpoints
└── schemas.py              # Request/response schemas
```

### 7.3 Core Components

**JWT Verification**:
- Extract token from "Authorization: Bearer" header
- Decode JWT using SECRET_KEY
- Verify signature
- Check expiration
- Extract user_id from "sub" claim
- Return 401 if invalid

**Database Layer**:
- SQLModel ORM for queries
- Async/await for non-blocking I/O
- Connection pooling
- Query optimization with indexes

**Route Handlers**:
- Dependency injection for JWT
- Dependency injection for database session
- User ownership verification
- Input validation
- Error handling

### 7.4 Deployment Considerations

**Environment Variables**:
```
DATABASE_URL=postgresql+asyncpg://...
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development|production
```

**HTTPS**:
- Enforce in production
- Valid SSL certificate
- HSTS header

**Logging**:
- Log authentication failures
- Log API requests
- Log errors
- No sensitive data in logs

---

## Part 8: Non-Functional Requirements

### 8.1 Performance

- [ ] API response time < 500ms (p95)
- [ ] Database queries < 200ms (p95)
- [ ] Frontend page load < 3s
- [ ] Support 100+ concurrent users
- [ ] List 1000 tasks without performance degradation

### 8.2 Scalability

- [ ] Stateless backend (can scale horizontally)
- [ ] Database optimized (indexes, queries)
- [ ] No in-memory state
- [ ] Ready for microservices split

### 8.3 Security

- [ ] JWT verification on every request
- [ ] User isolation enforced at DB + API
- [ ] HTTPS in production
- [ ] No plaintext passwords
- [ ] No data leakage in errors
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (React auto-escape)

### 8.4 Reliability

- [ ] Database backups (automatic)
- [ ] Error handling for network failures
- [ ] Graceful degradation
- [ ] Data consistency

### 8.5 Maintainability

- [ ] Clear code structure
- [ ] Type safety (TypeScript + Python typing)
- [ ] Comprehensive documentation
- [ ] Testable components
- [ ] Clear separation of concerns

---

## Part 9: Acceptance Criteria

### Feature: User Authentication

- [ ] Users can sign up with email & password
- [ ] Users can log in with email & password
- [ ] JWT token issued on successful login
- [ ] Frontend stores JWT securely
- [ ] Expired tokens trigger re-login

### Feature: Task CRUD

- [ ] Users can create tasks with title
- [ ] Users can view all their tasks
- [ ] Users can view single task details
- [ ] Users can update task fields
- [ ] Users can delete tasks
- [ ] Users can toggle task completion

### Feature: Authorization

- [ ] API returns 401 for missing JWT
- [ ] API returns 401 for invalid JWT
- [ ] API returns 401 for expired JWT
- [ ] API returns 400 if URL user_id ≠ JWT user_id
- [ ] API returns 404 for unauthorized tasks
- [ ] User A cannot access User B's tasks

### Feature: Data Isolation

- [ ] Users see only their own tasks
- [ ] Task list filtered by authenticated user
- [ ] Statistics show only user's tasks
- [ ] Cross-user modification returns 404

### Feature: API Design

- [ ] Endpoints follow REST conventions
- [ ] Responses use proper HTTP status codes
- [ ] Error responses include detail message
- [ ] CORS configured correctly
- [ ] Request validation works

---

## Part 10: Deliverables

### Specification Deliverables

✅ This document (unified specification)
✅ API specification with endpoint details
✅ Database schema with relationships
✅ Frontend requirements & components
✅ Backend requirements & structure
✅ Security specification
✅ Acceptance criteria

### Implementation Deliverables (via Agents)

✅ Backend API code (FastAPI)
✅ Frontend code (Next.js + React)
✅ Database models (SQLModel)
✅ Authentication middleware
✅ API client wrapper
✅ UI components
✅ Configuration & setup

### Testing Deliverables

✅ Integration test checklist
✅ Security test scenarios
✅ User isolation verification
✅ API endpoint validation
✅ Error handling tests

### Documentation Deliverables

✅ API documentation
✅ Database schema docs
✅ Architecture overview
✅ Setup & deployment guide
✅ Security report

---

## Part 11: Development Methodology

### Spec-Driven Development

1. ✅ **Specification First**: This document defines all requirements
2. ✅ **Agent-Driven**: Specialized agents implement each component
3. ✅ **Execution Order**: Agents follow defined sequence
4. ✅ **No Manual Coding**: All code generated via Claude Code
5. ✅ **Comprehensive Testing**: Security & functionality tests

### Agent Execution Order

```
1. Spec Writer Agent (done - this spec)
   ↓
2. Architecture Planner Agent (design system)
   ↓
3. Database Engineer Agent (SQLModel + schema)
   ↓
4. Backend Engineer Agent (FastAPI endpoints)
   ↓
5. Frontend Engineer Agent (Next.js UI)
   ↓
6. Integration & Security Tester Agent (validation)
```

---

## Part 12: Constraints & Rules

### Development Constraints

- ✅ All code generated via Claude Code
- ✅ No hand-written endpoints
- ✅ No hand-written components
- ✅ Specifications are authoritative
- ✅ Agents follow execution order

### Technical Constraints

- ✅ Backend must be stateless
- ✅ Frontend uses JWT for auth
- ✅ Database is Neon PostgreSQL
- ✅ API is REST-based
- ✅ Communication via JWT-secured REST

### API Constraints

- ✅ All endpoints require JWT
- ✅ User_id in URL must match JWT
- ✅ Responses use JSON
- ✅ Errors include detail message
- ✅ CORS properly configured

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-07 | Initial specification |
| 2.0 | 2026-02-08 | Unified specification with detailed API, user_id in URL |

---

## Approval & Sign-Off

**Specification Status**: ✅ APPROVED FOR IMPLEMENTATION

**By**: Spec-Kit Plus Framework  
**Date**: 2026-02-08  
**Valid From**: 2026-02-08  
**Valid Until**: End of Phase II

---

## Next Steps

This specification is now ready for implementation by the agent team:

1. **Architecture Planner Agent** designs the system
2. **Database Engineer Agent** implements SQLModel models
3. **Backend Engineer Agent** implements FastAPI endpoints
4. **Frontend Engineer Agent** implements Next.js UI
5. **Integration Tester Agent** validates complete system

All implementation must strictly follow this specification. Deviations require specification amendments.

---

**Document Owner**: Phase II Project Lead  
**Maintained By**: Specification Framework  
**Last Updated**: 2026-02-08
