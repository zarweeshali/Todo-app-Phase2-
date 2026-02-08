# Frontend Skills & Capabilities

**Framework**: Next.js 14+ (App Router)  
**Language**: TypeScript  
**Styling**: Tailwind CSS  
**Status**: Production Ready

---

## Core Skills

### 1. Next.js App Router
- ✅ File-based routing
- ✅ Server & client components
- ✅ Metadata configuration
- ✅ Dynamic routes
- ✅ Layout system

### 2. React Components
- ✅ Functional components with hooks
- ✅ useState for local state
- ✅ useEffect for side effects
- ✅ Custom hooks
- ✅ Component composition

### 3. JWT Token Handling
- ✅ Token extraction from storage
- ✅ Automatic Bearer token injection
- ✅ Token refresh handling
- ✅ Error handling on 401
- ✅ Session management

### 4. API Integration
- ✅ Fetch API with custom wrapper
- ✅ Error handling & types
- ✅ Loading states
- ✅ Request cancellation support
- ✅ TypeScript type safety

### 5. Tailwind CSS Styling
- ✅ Responsive design (mobile-first)
- ✅ Component styling
- ✅ Dark mode support (configurable)
- ✅ Animation & transitions
- ✅ Accessibility-focused classes

### 6. Form Handling
- ✅ Form submission
- ✅ Input validation
- ✅ Error messages
- ✅ Loading states
- ✅ Auto-clear after submit

---

## Implementation Examples

### API Client with JWT Injection
```typescript
async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const token = await getAuthToken();  // From Better Auth
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Authorization": `Bearer ${token}`,  // Automatic injection
      ...options?.headers,
    },
  });
  
  if (!response.ok) throw new Error("Request failed");
  return response.json();
}
```

### Reusable Todo Component
```typescript
export default function TodoItem({ todo, onToggle, onDelete }) {
  const [isLoading, setIsLoading] = useState(false);
  
  async function handleToggle() {
    setIsLoading(true);
    await onToggle(todo);  // Automatic API call
    setIsLoading(false);
  }
  
  return (
    <div className="flex items-center gap-3">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={handleToggle}
        disabled={isLoading}
      />
      <span>{todo.title}</span>
    </div>
  );
}
```

### Responsive Tailwind Layout
```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Mobile: 1 column, Tablet: 2 columns, Desktop: 3 columns */}
</div>
```

---

## Component Architecture

### Page Components
- `app/page.tsx` - Main todo list interface

### UI Components
- `components/TodoForm.tsx` - Create todo input
- `components/TodoList.tsx` - List wrapper
- `components/TodoItem.tsx` - Individual todo with actions
- `components/TodoStats.tsx` - Statistics display

### Utilities
- `lib/api.ts` - Centralized API calls with JWT
- `types/index.ts` - TypeScript type definitions

---

## Features Implemented
- ✅ Create todos with form validation
- ✅ List todos with filtering (all/completed/pending)
- ✅ Toggle completion status
- ✅ Edit todo titles
- ✅ Delete todos with confirmation
- ✅ Show progress statistics
- ✅ Loading & error states
- ✅ Responsive design

---

## Security Features
- ✅ Automatic JWT injection on all requests
- ✅ 401 handling for expired tokens
- ✅ No sensitive data in localStorage (depends on Better Auth)
- ✅ React auto-escapes HTML (XSS prevention)
- ✅ No direct DOM manipulation

---

## Performance Optimizations
- ✅ Lazy component loading
- ✅ Optimized re-renders with hooks
- ✅ Tailwind CSS purging for production
- ✅ Static generation where possible
- ✅ Image optimization (Next.js built-in)

---

## Testing Capabilities
- Unit tests for components
- Integration tests for user flows
- E2E tests with Playwright
- API mocking for tests

---

**Status**: Fully Implemented ✅
