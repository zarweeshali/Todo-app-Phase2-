# API Specification: Phase II Todo App

**Server**: FastAPI + Neon PostgreSQL  
**Authentication**: JWT Bearer Token  
**Base URL**: `http://localhost:8000/api`  
**Status**: Finalized

---

## Authentication

All endpoints (except `/health` and `/`) require JWT Bearer token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

**Token Claims**:
```json
{
  "sub": "user-uuid",
  "exp": 1234567890,
  "iat": 1234567800
}
```

**Security Enforcement**:
- ✅ User can only access/modify their own todos
- ✅ Ownership verified on every request via `user_id` from token
- ✅ 404 returned if todo belongs to different user

---

## Endpoints

### 1. Create Todo

```
POST /api/todos
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "title": "Buy groceries",
  "completed": false
}

Response: 201 Created
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "completed": false,
  "user_id": "660e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-02-08T10:30:00",
  "updated_at": "2026-02-08T10:30:00"
}
```

**Status Codes**:
- `201 Created`: Todo successfully created
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: User not found
- `422 Unprocessable Entity`: Validation error (empty title, etc.)

---

### 2. List Todos

```
GET /api/todos?status_filter=all
Authorization: Bearer <token>

Query Parameters:
- status_filter: "all" | "completed" | "pending" (default: "all")

Response: 200 OK
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "completed": false,
    "user_id": "660e8400-e29b-41d4-a716-446655440000",
    "created_at": "2026-02-08T10:30:00",
    "updated_at": "2026-02-08T10:30:00"
  }
]
```

**Status Codes**:
- `200 OK`: Successfully retrieved todos
- `401 Unauthorized`: Invalid or missing token

---

### 3. Get Single Todo

```
GET /api/todos/{todo_id}
Authorization: Bearer <token>

Response: 200 OK
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "completed": false,
  "user_id": "660e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-02-08T10:30:00",
  "updated_at": "2026-02-08T10:30:00"
}
```

**Status Codes**:
- `200 OK`: Todo retrieved
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Todo not found or doesn't belong to user

---

### 4. Update Todo

```
PUT /api/todos/{todo_id}
Authorization: Bearer <token>
Content-Type: application/json

Request Body (partial update):
{
  "title": "Buy groceries and cook dinner",
  "completed": true
}

Response: 200 OK
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and cook dinner",
  "completed": true,
  "user_id": "660e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-02-08T10:30:00",
  "updated_at": "2026-02-08T11:00:00"
}
```

**Status Codes**:
- `200 OK`: Todo updated
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Todo not found or doesn't belong to user
- `422 Unprocessable Entity`: Validation error

---

### 5. Delete Todo

```
DELETE /api/todos/{todo_id}
Authorization: Bearer <token>

Response: 204 No Content
```

**Status Codes**:
- `204 No Content`: Todo deleted
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Todo not found or doesn't belong to user

---

### 6. Get Todo Statistics

```
GET /api/todos/{todo_id}/stats
Authorization: Bearer <token>

Response: 200 OK
{
  "total": 10,
  "completed": 3,
  "pending": 7
}
```

**Status Codes**:
- `200 OK`: Statistics retrieved
- `401 Unauthorized`: Invalid or missing token

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message explaining what went wrong"
}
```

### Common Errors

| Status | Detail | Cause |
|--------|--------|-------|
| 401 | Token has expired | JWT token expired |
| 401 | Invalid token | Malformed or tampered JWT |
| 401 | Missing user_id | Token missing required claim |
| 404 | Todo not found | Todo doesn't exist or belongs to another user |
| 422 | String should have at least 1 character | Empty todo title |
| 422 | String should have at most 500 characters | Todo title too long |

---

## Implementation Details

- **Async**: All endpoints use async/await for non-blocking I/O
- **Transactions**: All database operations are transactional
- **Validation**: Input validated using Pydantic/SQLModel
- **CORS**: Configured to allow frontend from localhost:3000 and 5173 (Vite)
- **Health Check**: `GET /health` available without authentication

---

## Environment Variables

```bash
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
FRONTEND_URL=https://yourdomain.com  # Optional, for production CORS
```
