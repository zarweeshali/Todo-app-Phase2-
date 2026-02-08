# Database Schema Specification: Phase II

**Technology**: Neon PostgreSQL + SQLModel  
**Created**: 2026-02-08  
**Status**: Finalized

## Database Design

### User Table

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE INDEX idx_users_email ON users(email);
```

### Todo Table

```sql
CREATE TABLE todos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(500) NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_user_completed ON todos(user_id, completed);
```

## SQLModel Entities

### User Entity
- `id`: UUID (primary key)
- `email`: String (unique, required)
- `name`: String (optional)
- `todos`: Relationship to Todo (cascade delete)
- `created_at`: DateTime
- `updated_at`: DateTime

### Todo Entity
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key, required)
- `title`: String (1-500 chars, required)
- `completed`: Boolean (default: False)
- `user`: Relationship back to User
- `created_at`: DateTime
- `updated_at`: DateTime

## Ownership Rules

✅ **Data Isolation**: Users can only access their own todos
✅ **Cascading**: Deleting a user deletes all their todos
✅ **Indexes**: Optimized for `todos.user_id` and `(user_id, completed)` queries

## Neon Connection

- **Provider**: Neon PostgreSQL
- **Environment Variable**: `DATABASE_URL`
- **Connection Pool**: SQLAlchemy connection pooling
- **SSL**: Enabled by default in Neon

## Migration Strategy

- Use Alembic for schema versioning
- Initial migration: Create users & todos tables
