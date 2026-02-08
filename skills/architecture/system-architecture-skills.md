# Architecture Skills & Capabilities

**Focus**: System Design, Full-Stack Integration, Best Practices  
**Status**: Production Ready

---

## Core Architecture Skills

### 1. Full-Stack Design
- ✅ Monolithic vs microservices decision
- ✅ API contract definition
- ✅ Frontend-backend separation
- ✅ Data flow design
- ✅ Scalability planning

### 2. Authentication Architecture
- ✅ Stateless JWT design
- ✅ Token generation & validation flow
- ✅ User context propagation
- ✅ Session management
- ✅ Multi-tenant support (prep)

### 3. Database Architecture
- ✅ Schema design principles
- ✅ Normalization & denormalization
- ✅ Relationship modeling
- ✅ Indexing strategy
- ✅ Query optimization

### 4. API Design
- ✅ RESTful principles
- ✅ Resource-oriented design
- ✅ HTTP method selection
- ✅ Status code semantics
- ✅ Error handling patterns

### 5. Frontend Architecture
- ✅ Component hierarchy
- ✅ State management
- ✅ API client abstraction
- ✅ Error boundary patterns
- ✅ Performance optimization

### 6. Security Architecture
- ✅ Defense in depth
- ✅ Data isolation patterns
- ✅ Trust boundaries
- ✅ Threat modeling
- ✅ Security by default

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Client (Browser)                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │ React Components (Next.js App Router)            │   │
│  │ - TodoForm: Create/edit interface                │   │
│  │ - TodoList: Display todos                        │   │
│  │ - TodoStats: Show progress                       │   │
│  │ ├─ State: useState hooks                         │   │
│  │ └─ Side effects: useEffect hooks                 │   │
│  ├──────────────────────────────────────────────────┤   │
│  │ API Client Layer                                 │   │
│  │ - Fetch wrapper with JWT injection               │   │
│  │ - Error handling & type safety                   │   │
│  │ - Loading state management                       │   │
│  ├──────────────────────────────────────────────────┤   │
│  │ Storage & Auth                                   │   │
│  │ - localStorage: tokens                           │   │
│  │ - Better Auth: session management                │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────┬──────────────────────────────────────┘
                 │ HTTPS + Bearer JWT Token
                 ▼
┌─────────────────────────────────────────────────────────┐
│             Backend (FastAPI Server)                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Request Pipeline                                 │   │
│  │ 1. Receive HTTP request                          │   │
│  │ 2. Extract JWT token                             │   │
│  │ 3. Verify signature & expiration                 │   │
│  │ 4. Extract user_id                               │   │
│  ├──────────────────────────────────────────────────┤   │
│  │ Route Handlers                                   │   │
│  │ - POST /api/todos (Create)                       │   │
│  │ - GET /api/todos (List)                          │   │
│  │ - PUT /api/todos/{id} (Update)                   │   │
│  │ - DELETE /api/todos/{id} (Delete)                │   │
│  │ ├─ All handlers filter by user_id                │   │
│  │ └─ Return 404 if unauthorized                    │   │
│  ├──────────────────────────────────────────────────┤   │
│  │ Database Layer                                   │   │
│  │ - SQLModel ORM                                   │   │
│  │ - Async SQLAlchemy                               │   │
│  │ - Connection pooling                             │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────┬──────────────────────────────────────┘
                 │ SQL Queries
                 ▼
         ┌───────────────────┐
         │  Neon PostgreSQL  │
         │                   │
         │ ┌───────────────┐ │
         │ │ users table   │ │
         │ │ - id (PK)     │ │
         │ │ - email       │ │
         │ │ - created_at  │ │
         │ └───────────────┘ │
         │ ┌───────────────┐ │
         │ │ todos table   │ │
         │ │ - id (PK)     │ │
         │ │ - user_id(FK) │ │
         │ │ - title       │ │
         │ │ - completed   │ │
         │ └───────────────┘ │
         └───────────────────┘
```

---

## Design Patterns Used

### 1. Dependency Injection (FastAPI)
```python
# JWT verification is injected as dependency
@app.get("/api/todos")
async def list_todos(
    user_id: UUID = Depends(verify_token),        # Auto-verified
    session: AsyncSession = Depends(get_session),  # Auto-provided
):
    # No manual verification needed
    pass
```

### 2. Factory Pattern (API Client)
```typescript
// Single API client factory for all endpoints
const todoApi = {
  create: (todo) => fetchApi("/todos", { method: "POST", body: todo }),
  list: (filter) => fetchApi(`/todos?status_filter=${filter}`),
  delete: (id) => fetchApi(`/todos/${id}`, { method: "DELETE" }),
};
```

### 3. Repository Pattern (Database)
```python
# All queries go through repository methods
class TodoRepository:
    async def get_by_user(self, user_id: UUID) -> List[Todo]:
        # User isolation enforced here
        pass
    
    async def update(self, todo_id: UUID, user_id: UUID, **updates):
        # Ownership verified here
        pass
```

### 4. Component Composition (React)
```typescript
<TodoList>
  {todos.map(todo => 
    <TodoItem 
      todo={todo} 
      onToggle={handleToggle}
      onDelete={handleDelete}
    />
  )}
</TodoList>
```

---

## Data Flow

### Create Todo Flow
```
User Input (Form)
    ↓
Form Validation (Frontend)
    ↓
API Call: POST /api/todos (with JWT)
    ↓
JWT Verification (Backend)
    ↓
Input Validation (Pydantic)
    ↓
Database Insert (SQLModel)
    ↓
Return 201 + Todo Object
    ↓
Update UI (React re-render)
```

### User Isolation Flow
```
User B requests User A's Todo
    ↓
GET /api/todos/user-a-todo-id (with User B's JWT)
    ↓
Extract user_id from token → "user-b-id"
    ↓
Query: SELECT * FROM todos WHERE id=X AND user_id="user-b-id"
    ↓
Result: No rows found
    ↓
Return 404 Not Found
```

---

## Scalability Considerations

### Current Design (Single Instance)
- ✅ Suitable for small to medium workload
- ✅ Simple deployment
- ✅ Easy debugging
- ⚠️ Single point of failure

### Future Scaling (Horizontal)
- ✅ Stateless JWT enables multiple servers
- ✅ Shared PostgreSQL database
- ✅ Separate API server instances
- ✅ Load balancer distributes traffic

### Future Scaling (Microservices)
- ✅ Auth service (Better Auth)
- ✅ Todo service (separate API)
- ✅ User service (profiles)
- ✅ Message queue (events)

---

## Architecture Trade-offs

### Choice: Stateless JWT
**Pros**:
- ✅ Scalable (no session state)
- ✅ Distributed systems friendly
- ✅ Mobile-friendly

**Cons**:
- ⚠️ Can't revoke immediately (on logout)
- ⚠️ Token size increases with claims

### Choice: Monolithic Backend
**Pros**:
- ✅ Simple deployment
- ✅ Easy debugging
- ✅ Direct database access

**Cons**:
- ⚠️ Scales everything together
- ⚠️ Single point of failure
- ⚠️ Technology locked-in

### Choice: Next.js Frontend
**Pros**:
- ✅ Server-side rendering option
- ✅ API routes for BFF pattern
- ✅ Image optimization
- ✅ Static generation

**Cons**:
- ⚠️ More complex deployment
- ⚠️ Larger bundle
- ⚠️ Learning curve

---

## Performance Architecture

### Optimization Strategies
1. **Database Level**
   - Indexes on user_id
   - Connection pooling
   - Query optimization

2. **API Level**
   - Async/await for non-blocking
   - Pagination for large lists
   - Caching headers

3. **Frontend Level**
   - Component memoization
   - Lazy loading routes
   - Tailwind CSS purging

---

## High Availability Architecture

### For Production
```
┌─────────────────────────────────┐
│      Reverse Proxy (Nginx)      │  Load balancer
├─────────────────────────────────┤
│  FastAPI Instance 1             │
│  FastAPI Instance 2             │  Horizontal scaling
│  FastAPI Instance 3             │
├─────────────────────────────────┤
│  Neon PostgreSQL (managed)      │  Database + backups
└─────────────────────────────────┘
```

---

## Disaster Recovery

### Backup Strategy
- [ ] Database automated backups (daily)
- [ ] Code version control (GitHub)
- [ ] Container registry (Docker Hub)
- [ ] Configuration management (env vars)

### Recovery Procedures
- [ ] Database restore from backup
- [ ] Code rollback to previous version
- [ ] Infrastructure rebuild

---

**Status**: Complete Architecture Design ✅
