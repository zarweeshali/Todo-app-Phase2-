# Integration Test Checklist: Phase II Todo App

**Status**: Comprehensive Testing Framework  
**Created**: 2026-02-08  
**Scope**: End-to-end user flows, API contract validation, security enforcement

---

## 1. Authentication & JWT Verification Tests

### 1.1 Token Creation

- [ ] **Test**: User logs in via Better Auth
  - **Expected**: JWT token is issued
  - **Verification**: Token contains user_id in claims
  - **Pass Criteria**: `token.sub === user_id`

- [ ] **Test**: Token has correct expiration
  - **Expected**: Token expires in 24 hours
  - **Verification**: `exp` claim is correct
  - **Pass Criteria**: `exp = now + 24h`

### 1.2 Token Validation on API Calls

- [ ] **Test**: Request with valid token
  - **Expected**: 200 OK response
  - **Method**: `GET /api/todos`
  - **Header**: `Authorization: Bearer {valid_token}`
  - **Pass Criteria**: Returns user's todos

- [ ] **Test**: Request with no token
  - **Expected**: 401 Unauthorized
  - **Method**: `GET /api/todos`
  - **Header**: None
  - **Pass Criteria**: `detail: "No authentication token"`

- [ ] **Test**: Request with invalid token
  - **Expected**: 401 Unauthorized
  - **Method**: `GET /api/todos`
  - **Header**: `Authorization: Bearer invalid_token_xyz`
  - **Pass Criteria**: `detail: "Invalid token"`

- [ ] **Test**: Request with expired token
  - **Expected**: 401 Unauthorized
  - **Method**: `GET /api/todos`
  - **Token**: Expired JWT
  - **Pass Criteria**: `detail: "Token has expired"`

- [ ] **Test**: Request with malformed Authorization header
  - **Expected**: 401 Unauthorized
  - **Header**: `Authorization: InvalidFormat token`
  - **Pass Criteria**: Error returned

### 1.3 Token Refresh & Renewal

- [ ] **Test**: Token refresh before expiration
  - **Expected**: New token issued
  - **Verification**: Old token still valid, new token issued
  - **Pass Criteria**: Both tokens work

---

## 2. User Isolation Tests (Critical Security)

### 2.1 CRUD Operation Isolation

- [ ] **Test**: User A cannot see User B's todos
  - **Setup**: Create User A and User B, User A creates 3 todos
  - **Action**: User B calls `GET /api/todos` with their token
  - **Expected**: Returns empty list or only User B's todos
  - **Pass Criteria**: User B's response doesn't include User A's todos

- [ ] **Test**: User A cannot update User B's todo
  - **Setup**: User A creates todo ID=X, User B has token
  - **Action**: User B calls `PUT /api/todos/X` with User B's token
  - **Expected**: 404 Not Found
  - **Pass Criteria**: Todo not modified, 404 returned

- [ ] **Test**: User A cannot delete User B's todo
  - **Setup**: User A creates todo ID=X, User B has token
  - **Action**: User B calls `DELETE /api/todos/X` with User B's token
  - **Expected**: 404 Not Found
  - **Pass Criteria**: Todo not deleted, 404 returned

- [ ] **Test**: User A cannot directly access User B's todo
  - **Setup**: User A creates todo ID=X
  - **Action**: User B calls `GET /api/todos/X` with User B's token
  - **Expected**: 404 Not Found
  - **Pass Criteria**: Todo details not exposed

### 2.2 Filter Isolation

- [ ] **Test**: Status filter only returns user's todos
  - **Setup**: User A has 2 completed + 3 pending, User B has 1 completed
  - **Action**: User B calls `GET /api/todos?status_filter=completed`
  - **Expected**: Only User B's 1 completed todo
  - **Pass Criteria**: Count = 1, no cross-user data

- [ ] **Test**: Statistics show only user's data
  - **Setup**: User A has 10 todos, User B has 0
  - **Action**: User B calls stats endpoint
  - **Expected**: `total: 0, completed: 0, pending: 0`
  - **Pass Criteria**: No data leakage

---

## 3. CRUD Operations Tests

### 3.1 Create Todo

- [ ] **Test**: Create todo with valid title
  - **Payload**: `{ "title": "Buy groceries", "completed": false }`
  - **Expected**: 201 Created
  - **Pass Criteria**: Todo in response with id, timestamps, user_id

- [ ] **Test**: Create todo with minimum title (1 char)
  - **Payload**: `{ "title": "A" }`
  - **Expected**: 201 Created
  - **Pass Criteria**: Accepted

- [ ] **Test**: Create todo with maximum title (500 chars)
  - **Payload**: `{ "title": "x" * 500 }`
  - **Expected**: 201 Created
  - **Pass Criteria**: Accepted

- [ ] **Test**: Create todo with empty title
  - **Payload**: `{ "title": "" }`
  - **Expected**: 422 Unprocessable Entity
  - **Pass Criteria**: Validation error returned

- [ ] **Test**: Create todo with title > 500 chars
  - **Payload**: `{ "title": "x" * 501 }`
  - **Expected**: 422 Unprocessable Entity
  - **Pass Criteria**: Validation error returned

- [ ] **Test**: Create todo with no title field
  - **Payload**: `{ "completed": false }`
  - **Expected**: 422 Unprocessable Entity
  - **Pass Criteria**: Required field error

- [ ] **Test**: Create todo with special characters
  - **Payload**: `{ "title": "Test™ 中文 🎉 <script>" }`
  - **Expected**: 201 Created
  - **Pass Criteria**: Special chars preserved, no XSS

### 3.2 List Todos

- [ ] **Test**: List with no todos
  - **Setup**: Fresh user account
  - **Action**: `GET /api/todos`
  - **Expected**: `[]` (empty array)
  - **Pass Criteria**: 200 OK, empty list

- [ ] **Test**: List all todos (default filter)
  - **Setup**: User has 5 todos (3 completed, 2 pending)
  - **Action**: `GET /api/todos`
  - **Expected**: All 5 todos
  - **Pass Criteria**: Count = 5

- [ ] **Test**: List completed todos only
  - **Setup**: User has 5 todos (3 completed, 2 pending)
  - **Action**: `GET /api/todos?status_filter=completed`
  - **Expected**: 3 completed todos
  - **Pass Criteria**: Only completed returned

- [ ] **Test**: List pending todos only
  - **Setup**: User has 5 todos (3 completed, 2 pending)
  - **Action**: `GET /api/todos?status_filter=pending`
  - **Expected**: 2 pending todos
  - **Pass Criteria**: Only pending returned

- [ ] **Test**: Order is creation order (newest first or oldest first)
  - **Setup**: Create todos A, B, C with delays
  - **Action**: `GET /api/todos`
  - **Expected**: Consistent ordering
  - **Pass Criteria**: Order is predictable/documented

### 3.3 Get Single Todo

- [ ] **Test**: Get existing todo
  - **Setup**: User has todo ID=X
  - **Action**: `GET /api/todos/X`
  - **Expected**: 200 OK, todo object
  - **Pass Criteria**: Correct todo returned

- [ ] **Test**: Get non-existent todo
  - **Action**: `GET /api/todos/non-existent-id`
  - **Expected**: 404 Not Found
  - **Pass Criteria**: Not found error

- [ ] **Test**: Get with invalid UUID format
  - **Action**: `GET /api/todos/invalid-uuid`
  - **Expected**: 400 Bad Request or 404
  - **Pass Criteria**: Error handled gracefully

### 3.4 Update Todo

- [ ] **Test**: Toggle completed status
  - **Setup**: Todo with `completed: false`
  - **Payload**: `{ "completed": true }`
  - **Expected**: 200 OK, `completed: true`
  - **Pass Criteria**: Status toggled

- [ ] **Test**: Update title
  - **Setup**: Todo with `title: "Old"`
  - **Payload**: `{ "title": "New Title" }`
  - **Expected**: 200 OK, title updated
  - **Pass Criteria**: Title changed, other fields unchanged

- [ ] **Test**: Update both title and completed
  - **Payload**: `{ "title": "New", "completed": true }`
  - **Expected**: Both fields updated
  - **Pass Criteria**: Both changes applied

- [ ] **Test**: Update with empty title
  - **Payload**: `{ "title": "" }`
  - **Expected**: 422 Unprocessable Entity
  - **Pass Criteria**: Validation error

- [ ] **Test**: Update with title > 500 chars
  - **Payload**: `{ "title": "x" * 501 }`
  - **Expected**: 422 Unprocessable Entity
  - **Pass Criteria**: Validation error

- [ ] **Test**: Partial update (only title, not completed)
  - **Setup**: Todo with `completed: false, title: "X"`
  - **Payload**: `{ "title": "Y" }`
  - **Expected**: Title updated, completed still false
  - **Pass Criteria**: Partial updates work

### 3.5 Delete Todo

- [ ] **Test**: Delete existing todo
  - **Setup**: User has todo ID=X
  - **Action**: `DELETE /api/todos/X`
  - **Expected**: 204 No Content
  - **Pass Criteria**: Todo removed from list

- [ ] **Test**: Verify todo is deleted
  - **Setup**: Delete todo ID=X
  - **Action**: `GET /api/todos/X`
  - **Expected**: 404 Not Found
  - **Pass Criteria**: Confirmed deleted

- [ ] **Test**: Delete non-existent todo
  - **Action**: `DELETE /api/todos/non-existent`
  - **Expected**: 404 Not Found
  - **Pass Criteria**: Proper error

- [ ] **Test**: Delete already deleted todo
  - **Setup**: Delete todo, then try again
  - **Expected**: 404 Not Found
  - **Pass Criteria**: Idempotent delete

---

## 4. Frontend Integration Tests

### 4.1 Page Load

- [ ] **Test**: Homepage loads without errors
  - **Action**: Navigate to `http://localhost:3000`
  - **Expected**: Page renders
  - **Pass Criteria**: No console errors

- [ ] **Test**: Requires authentication
  - **Action**: Access app without token
  - **Expected**: Redirects to login or shows error
  - **Pass Criteria**: Protected route

### 4.2 Todo Form

- [ ] **Test**: Create todo from UI
  - **Action**: Enter title, click "Add Todo"
  - **Expected**: Todo appears in list
  - **Pass Criteria**: Full create flow works

- [ ] **Test**: Form validation
  - **Action**: Try to submit empty form
  - **Expected**: Error or form prevents submit
  - **Pass Criteria**: Validation working

- [ ] **Test**: Form clears after submit
  - **Action**: Create todo, check input field
  - **Expected**: Input field is empty
  - **Pass Criteria**: UX is clean

### 4.3 Todo List

- [ ] **Test**: List displays all user todos
  - **Setup**: Create 5 todos via API
  - **Action**: Refresh page
  - **Expected**: All 5 appear
  - **Pass Criteria**: Data loads from backend

- [ ] **Test**: Filter buttons work
  - **Setup**: 3 completed, 2 pending todos
  - **Action**: Click "Completed" filter
  - **Expected**: Shows only 3
  - **Pass Criteria**: Filter functional

### 4.4 Todo Item Actions

- [ ] **Test**: Toggle completion
  - **Action**: Click checkbox
  - **Expected**: Todo marked complete, visual change
  - **Pass Criteria**: Toggle works

- [ ] **Test**: Edit todo
  - **Action**: Click edit, change title, save
  - **Expected**: Title updated
  - **Pass Criteria**: Edit flow works

- [ ] **Test**: Delete todo
  - **Action**: Click delete, confirm
  - **Expected**: Todo removed
  - **Pass Criteria**: Delete works

---

## 5. Error Handling Tests

### 5.1 Network Errors

- [ ] **Test**: API unreachable
  - **Setup**: Stop backend server
  - **Action**: Try to create todo
  - **Expected**: Error message shown
  - **Pass Criteria**: User informed of error

- [ ] **Test**: Timeout handling
  - **Setup**: Simulate slow network
  - **Action**: Create todo
  - **Expected**: Loading indicator, then error or success
  - **Pass Criteria**: No hanging requests

### 5.2 API Errors

- [ ] **Test**: 500 server error
  - **Setup**: Trigger server error (if possible)
  - **Expected**: Error message shown
  - **Pass Criteria**: Graceful error handling

---

## 6. Performance Tests

- [ ] **Test**: Load 1000 todos
  - **Setup**: Create many todos
  - **Action**: List all
  - **Expected**: Page remains responsive
  - **Pass Criteria**: No UI freeze

- [ ] **Test**: API response time < 500ms
  - **Action**: Time API calls
  - **Expected**: Response within 500ms
  - **Pass Criteria**: Acceptable performance

---

## Test Execution Checklist

### Phase 1: Unit/Integration (Per Feature)
- [ ] Auth tests pass
- [ ] JWT tests pass
- [ ] User isolation tests pass
- [ ] CRUD tests pass

### Phase 2: End-to-End
- [ ] Frontend integration tests pass
- [ ] Error handling tests pass

### Phase 3: Security
- [ ] No user data leakage
- [ ] JWT enforcement confirmed
- [ ] All edge cases handled

### Phase 4: Performance
- [ ] API response times acceptable
- [ ] UI renders smoothly

---

## Test Results Summary

| Category | Tests | Passed | Failed | Status |
|----------|-------|--------|--------|--------|
| Authentication | 10 | - | - | ⏳ Pending |
| User Isolation | 8 | - | - | ⏳ Pending |
| CRUD Operations | 25 | - | - | ⏳ Pending |
| Frontend Integration | 12 | - | - | ⏳ Pending |
| Error Handling | 5 | - | - | ⏳ Pending |
| Performance | 2 | - | - | ⏳ Pending |
| **TOTAL** | **62** | - | - | ⏳ Pending |

---

## Notes

- All tests should be automated where possible (Pytest, Jest, Playwright)
- Manual testing for UX verification
- Security tests are critical - prioritize user isolation
- Performance tests should use realistic data volumes
