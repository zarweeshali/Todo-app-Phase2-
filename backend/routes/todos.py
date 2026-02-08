"""
Todo endpoints for Phase II Todo App
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.sql import text

from backend.models import Todo, TodoCreate, TodoUpdate, TodoRead, User, Priority
from backend.db import get_session
from backend.auth import verify_token

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    user_id: UUID = Depends(verify_token),
    session: Session = Depends(get_session),
):
    """
    Create a new todo for the authenticated user.

    **Security**: User can only create todos for themselves (user_id from token)
    """
    # Verify user exists
    result = session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create todo
    db_todo = Todo(
        user_id=user_id,
        title=todo.title,
        completed=todo.completed,
        due_date=todo.due_date,
        priority=todo.priority
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get("", response_model=List[TodoRead])
def list_todos(
    user_id: UUID = Depends(verify_token),
    session: Session = Depends(get_session),
    status_filter: str = None,
    priority_filter: str = None,
    search: str = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    offset: int = 0,
    limit: int = 20,
):
    """
    Get all todos for the authenticated user with advanced filtering and pagination.

    **Security**: Users can only see their own todos (enforced by user_id from token)

    Query Parameters:
    - status_filter: Filter by status - "all" (default), "completed", or "pending"
    - priority_filter: Filter by priority - "low", "medium", "high"
    - search: Search in todo titles
    - sort_by: Sort by "created_at", "updated_at", "due_date", "priority", "title"
    - sort_order: Sort order "asc" or "desc"
    - offset: Pagination offset
    - limit: Page size (max 100)
    """
    # Validate limit
    if limit > 100:
        limit = 100

    query = select(Todo).where(Todo.user_id == user_id)

    # Apply status filter
    if status_filter == "completed":
        query = query.where(Todo.completed == True)
    elif status_filter == "pending":
        query = query.where(Todo.completed == False)

    # Apply priority filter
    if priority_filter:
        query = query.where(Todo.priority == priority_filter)

    # Apply search filter
    if search:
        query = query.where(func.lower(Todo.title).contains(func.lower(search)))

    # Apply sorting
    if sort_by == "due_date":
        sort_field = Todo.due_date
    elif sort_by == "priority":
        sort_field = Todo.priority
    elif sort_by == "title":
        sort_field = Todo.title
    elif sort_by == "updated_at":
        sort_field = Todo.updated_at
    else:  # default to created_at
        sort_field = Todo.created_at

    if sort_order == "asc":
        query = query.order_by(sort_field.asc())
    else:
        query = query.order_by(sort_field.desc())

    # Apply pagination
    query = query.offset(offset).limit(limit)

    result = session.execute(query)
    todos = result.scalars().all()

    return todos


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: UUID,
    user_id: UUID = Depends(verify_token),
    session: Session = Depends(get_session),
):
    """
    Get a specific todo by ID.

    **Security**: User can only access their own todos
    """
    result = session.execute(
        select(Todo).where(
            (Todo.id == todo_id) & (Todo.user_id == user_id)
        )
    )
    todo = result.scalars().first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    user_id: UUID = Depends(verify_token),
    session: Session = Depends(get_session),
):
    """
    Update a todo (title, completed status, due date, and/or priority).

    **Security**: User can only update their own todos
    """
    result = session.execute(
        select(Todo).where(
            (Todo.id == todo_id) & (Todo.user_id == user_id)
        )
    )
    db_todo = result.scalars().first()

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Update fields if provided
    if todo_update.title is not None:
        db_todo.title = todo_update.title

    if todo_update.completed is not None:
        db_todo.completed = todo_update.completed

    if todo_update.due_date is not None:
        db_todo.due_date = todo_update.due_date

    if todo_update.priority is not None:
        db_todo.priority = todo_update.priority

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: UUID,
    user_id: UUID = Depends(verify_token),
    session: Session = Depends(get_session),
):
    """
    Delete a todo.

    **Security**: User can only delete their own todos
    """
    result = session.execute(
        select(Todo).where(
            (Todo.id == todo_id) & (Todo.user_id == user_id)
        )
    )
    db_todo = result.scalars().first()

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    session.delete(db_todo)
    session.commit()

    return None


@router.get("/stats", response_model=dict)
def get_todo_stats(
    user_id: UUID = Depends(verify_token),
    session: Session = Depends(get_session),
):
    """
    Get todo statistics for the user.

    Returns:
    - total: Total number of todos
    - completed: Number of completed todos
    - pending: Number of pending todos
    - by_priority: Count of todos by priority
    - overdue: Number of overdue todos
    """
    result = session.execute(
        select(Todo).where(Todo.user_id == user_id)
    )
    todos = result.scalars().all()

    total = len(todos)
    completed = sum(1 for t in todos if t.completed)
    pending = total - completed
    
    # Count by priority
    low_count = sum(1 for t in todos if t.priority == Priority.LOW)
    medium_count = sum(1 for t in todos if t.priority == Priority.MEDIUM)
    high_count = sum(1 for t in todos if t.priority == Priority.HIGH)
    
    # Count overdue todos
    now = datetime.utcnow()
    overdue = sum(1 for t in todos if not t.completed and t.due_date and t.due_date < now)

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "by_priority": {
            "low": low_count,
            "medium": medium_count,
            "high": high_count
        },
        "overdue": overdue
    }
