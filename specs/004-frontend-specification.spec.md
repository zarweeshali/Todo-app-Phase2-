# Frontend Specification: Phase II Todo App (Next.js)

**Framework**: Next.js App Router  
**Styling**: Tailwind CSS  
**Authentication**: Better Auth (JWT)  
**Status**: Finalized

---

## Architecture

### Stack
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Auth**: Better Auth (JWT-enabled)
- **HTTP Client**: Fetch API with Bearer token injection
- **State Management**: React hooks (useState, useEffect)

---

## Authentication Flow

```
1. User logs in via Better Auth
   └─> Better Auth provides JWT token
   
2. JWT stored in localStorage/session storage
   └─> Accessible via getAuthToken()
   
3. Every API request includes JWT
   └─> Authorization: Bearer {token}
   
4. Backend validates JWT and user_id
   └─> Returns 401 if invalid
```

### Token Integration

All API calls automatically inject JWT via `fetchApi()` helper:

```typescript
async function fetchApi(endpoint, options) {
  const token = await getAuthToken();  // Get JWT
  
  // Add to Authorization header
  headers: {
    Authorization: `Bearer ${token}`,
    ...options.headers
  }
}
```

---

## Components Structure

### Pages (App Router)

| File | Route | Purpose |
|------|-------|---------|
| `app/page.tsx` | `/` | Todo list (main page) |
| `app/layout.tsx` | - | Root layout with Tailwind |

### Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `TodoForm` | `components/TodoForm.tsx` | Create new todos |
| `TodoList` | `components/TodoList.tsx` | Display todo list |
| `TodoItem` | `components/TodoItem.tsx` | Individual todo with actions |
| `TodoStats` | `components/TodoStats.tsx` | Summary statistics |

---

## API Client (`lib/api.ts`)

**Purpose**: Centralized API communication with JWT injection

### Methods

```typescript
todoApi.create(title: string) → Promise<TodoRead>
todoApi.list(filter: "all"|"completed"|"pending") → Promise<TodoRead[]>
todoApi.get(id: string) → Promise<TodoRead>
todoApi.update(id: string, updates: TodoUpdate) → Promise<TodoRead>
todoApi.delete(id: string) → Promise<void>
todoApi.getStats() → Promise<Stats>
```

### Features
- ✅ Automatic JWT injection
- ✅ Error handling with ApiError type
- ✅ Proper TypeScript types
- ✅ Environment variable configuration

---

## User Interface

### Main Page Flow

1. **Header** - App title and description
2. **Statistics** - Show total/completed/pending counts
3. **Error Alert** - Display errors if any
4. **Create Form** - Input field + Add button
5. **Filter Buttons** - Switch between all/completed/pending
6. **Todo List** - Display todos with actions

### Todo Item Actions

Each todo can:
- ✅ Toggle completed status (checkbox)
- ✏️ Edit title (edit button → input field)
- 🗑️ Delete with confirmation
- Display completion status with strikethrough

---

## Styling

### Design System

- **Colors**: 
  - Primary: Indigo (`indigo-600`)
  - Success: Green (`green-600`)
  - Warning: Orange (`orange-600`)
  - Error: Red (`red-600`)

- **Spacing**: Tailwind defaults
- **Responsive**: Mobile-first, all views work on small screens
- **Accessibility**: Proper labels, ARIA attributes where needed

### Key Classes Used

```css
/* Layout */
.container, .mx-auto, .px-4, .py-8

/* Backgrounds */
.bg-gradient-to-br .from-blue-50 .to-indigo-100
.bg-white, .bg-red-50

/* Typography */
.text-4xl .font-bold .text-gray-900

/* Interactions */
.rounded-md, .border, .shadow-sm
.hover:bg-indigo-700, .disabled:bg-gray-400

/* Forms */
.focus:border-indigo-500, .focus:outline-none
```

---

## File Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page (todo list)
│   └── globals.css         # Tailwind imports
├── components/
│   ├── TodoForm.tsx        # Create todo form
│   ├── TodoList.tsx        # Todo list wrapper
│   ├── TodoItem.tsx        # Individual todo
│   └── TodoStats.tsx       # Statistics display
├── lib/
│   └── api.ts              # API client with JWT
├── types/
│   └── index.ts            # TypeScript types
├── styles/
│   └── globals.css         # Global styles
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.ts
├── next.config.js
├── .env.local.example      # Environment template
└── auth.config.py          # Better Auth config
```

---

## Environment Configuration

### `.env.local`

```bash
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Better Auth
NEXT_PUBLIC_AUTH_URL=http://localhost:3000/auth
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_DATABASE_URL=postgresql+asyncpg://...
```

---

## Development Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
cd frontend
cp .env.local.example .env.local
npm install
```

### Development Server

```bash
npm run dev
```

Server runs at `http://localhost:3000`

### Build for Production

```bash
npm run build
npm run start
```

---

## Features Implemented

### ✅ Todo Management
- Create todos with title
- View all todos with filtering
- Mark todos as complete/incomplete
- Edit todo titles
- Delete todos with confirmation
- Display progress statistics

### ✅ Authentication
- JWT token injection on all API calls
- Automatic token refresh (if Better Auth enabled)
- Secure token storage

### ✅ UX
- Loading states on actions
- Error messages display
- Empty state message
- Responsive design
- Progress bar with percentage

### ✅ Performance
- Client-side rendering
- Optimistic updates possible
- Minimal re-renders with React hooks
- Tailwind CSS (production-optimized)

---

## Security Considerations

1. **Token Storage**: Tokens stored in localStorage (configurable with Better Auth)
2. **HTTPS**: Use in production (enforce via environment)
3. **CORS**: Frontend configured to communicate with backend safely
4. **XSS Protection**: React escapes HTML by default
5. **CSRF**: Not needed with stateless JWT auth

---

## Future Enhancements

- [ ] Offline mode with service workers
- [ ] Real-time sync with WebSockets
- [ ] Drag-and-drop reordering
- [ ] Categories/tags for todos
- [ ] Notifications
- [ ] Dark mode toggle

---

## Troubleshooting

### API calls fail with "No authentication token"
- Ensure Better Auth is configured
- Check token is being stored
- Verify `getAuthToken()` implementation

### Styling not applied
- Run `npm install`
- Delete `.next` folder and rebuild
- Check `tailwind.config.ts` includes correct paths

### CORS errors
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend CORS configuration
- Ensure backend is running on expected port
