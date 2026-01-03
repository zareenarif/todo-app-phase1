# Data Model: Phase I Todo Application

**Feature**: 001-todo-app
**Date**: 2026-01-03
**Status**: Complete

## Overview

The Phase I Todo Application uses a simple in-memory data model with a single entity: **Task**. The model adheres strictly to the Task Entity Rules defined in the project constitution.

## Entity: Task

### Purpose
Represents a single todo item that a user wants to track.

### Attributes

| Attribute | Type | Required | Default | Constraints | Mutability |
|-----------|------|----------|---------|-------------|------------|
| id | int | Yes | Auto-generated | Unique, positive integer | Immutable |
| title | str | Yes | None | Non-empty after whitespace strip | Mutable |
| description | str | No | None or "" | No length limit | Mutable |
| completed | bool | Yes | False | True or False | Mutable |

### Attribute Details

#### id
- **Type**: `int`
- **Purpose**: Unique identifier for the task
- **Generation**: Auto-incremented starting from 1
- **Immutability**: Once assigned, the ID never changes
- **Uniqueness**: Guaranteed unique within a session
- **Reuse**: IDs are NOT reused after task deletion (counter continues incrementing)
- **Validation**: Always positive integer (1, 2, 3, ...)

#### title
- **Type**: `str`
- **Purpose**: Brief description of what the task is about
- **Required**: Yes - cannot be empty or whitespace-only
- **Validation**:
  - Must not be empty string after `.strip()`
  - Whitespace-only strings (e.g., "   ") are invalid
  - No maximum length constraint (system memory is the limit)
- **Mutability**: Can be updated via Update Task operation
- **Display**: Shown in task lists and views

#### description
- **Type**: `str` or `None`
- **Purpose**: Optional detailed information about the task
- **Required**: No - can be empty, None, or omitted
- **Validation**: No validation required (any string accepted, including empty)
- **Mutability**: Can be updated via Update Task operation
- **Display**: Shown when viewing task details (may not appear in list view)

#### completed
- **Type**: `bool`
- **Purpose**: Tracks whether the task is done
- **Required**: Yes - always has a value
- **Default**: `False` (new tasks are pending)
- **Values**:
  - `False`: Task is pending/incomplete
  - `True`: Task is completed/done
- **Mutability**: Toggled via Mark Task Complete/Incomplete operation
- **Display**: Shown as "Pending" (False) or "Completed" (True)

## Python Class Structure

```python
class Task:
    """
    Represents a todo task item.

    Attributes:
        id (int): Unique task identifier (immutable)
        title (str): Task title (required, non-empty)
        description (str): Optional task description
        completed (bool): Completion status (default: False)
    """

    def __init__(self, task_id: int, title: str, description: str = None, completed: bool = False):
        """
        Initialize a new Task.

        Args:
            task_id: Unique integer identifier
            title: Task title (must be non-empty after strip)
            description: Optional description (default: None)
            completed: Completion status (default: False)

        Raises:
            ValueError: If title is empty after stripping whitespace
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        self._id = task_id  # Immutable (no setter)
        self.title = title.strip()
        self.description = description.strip() if description else None
        self.completed = completed

    @property
    def id(self) -> int:
        """Get task ID (immutable)."""
        return self._id

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"

    def __str__(self) -> str:
        """Human-readable string representation."""
        status = "Completed" if self.completed else "Pending"
        return f"[{self.id}] {self.title} - {status}"
```

## Data Storage Structure

### In-Memory Storage
The application maintains two data structures in the TodoService:

1. **Task List** (`list[Task]`):
   - Maintains insertion order for display
   - Allows iteration for "View Tasks"
   - Type: Python list

2. **Task Dictionary** (`dict[int, Task]`):
   - Maps task ID to Task object
   - Enables O(1) lookup for update/delete/toggle operations
   - Key: task ID (int)
   - Value: Task object

### Example Storage State

```python
# After adding 3 tasks:
_tasks = [
    Task(1, "Buy groceries", None, False),
    Task(2, "Fix bug", "Update validation logic", True),
    Task(3, "Write report", None, False)
]

_task_dict = {
    1: Task(1, "Buy groceries", None, False),
    2: Task(2, "Fix bug", "Update validation logic", True),
    3: Task(3, "Write report", None, False)
}

_next_id = 4  # Next ID to assign
```

## State Transitions

### Task Lifecycle

```
[Created] ---> [Pending] ---> [Completed] ---> [Deleted]
     ↑            ↓                ↓
     |            +------<---------+
     |                  (toggle)
     +-------------- (update) ------->
```

### Valid State Transitions

| From State | Action | To State | Notes |
|------------|--------|----------|-------|
| N/A | Add Task | Pending | New task created with completed=False |
| Pending | Mark Complete | Completed | Toggle completed to True |
| Completed | Mark Incomplete | Pending | Toggle completed to False |
| Any | Update Task | Same | Title/description changed, status unchanged |
| Any | Delete Task | Deleted | Task removed from storage |

### Immutable State
- **ID**: Never changes once assigned
- **Creation order**: Implicit in list position (not stored as attribute)

## Validation Rules

### At Creation (Add Task)
1. **Title validation**:
   - MUST NOT be None
   - MUST NOT be empty string after `.strip()`
   - Example violations: `""`, `"   "`, `None`
   - Example valid: `"Buy groceries"`, `"  Task  "` (becomes `"Task"`)

2. **ID validation**:
   - Automatically assigned (not user input)
   - Guaranteed unique and positive

3. **Description validation**:
   - No validation (optional field)
   - Accepts: None, empty string, any string

4. **Completed validation**:
   - Always False for new tasks (enforced by default)

### At Update (Update Task)
1. **Title validation**:
   - Same as creation: non-empty after strip
   - Can update to new non-empty value

2. **Description validation**:
   - Same as creation: no validation
   - Can update to any value including empty/None

3. **ID validation**:
   - Task with given ID MUST exist
   - Error if ID not found

### At Toggle (Mark Complete/Incomplete)
1. **ID validation**:
   - Task with given ID MUST exist
   - Error if ID not found

2. **Toggle logic**:
   - If currently False → set to True
   - If currently True → set to False

### At Delete (Delete Task)
1. **ID validation**:
   - Task with given ID MUST exist
   - Error if ID not found

## Error Conditions

| Condition | Error Message | HTTP Equiv (if applicable) |
|-----------|---------------|----------------------------|
| Empty title on create | "Task title cannot be empty" | 400 Bad Request |
| Empty title on update | "Task title cannot be empty" | 400 Bad Request |
| Task ID not found | "Task with ID {id} not found" | 404 Not Found |
| Invalid ID format (non-int) | "Invalid task ID" | 400 Bad Request |

## Data Constraints Summary

### Hard Constraints (Enforced by Code)
- ✅ ID is unique (enforced by auto-increment)
- ✅ ID is immutable (enforced by property with no setter)
- ✅ Title is non-empty (enforced by validation)
- ✅ Completed is boolean (enforced by type)

### Soft Constraints (No Enforcement)
- ⚠️ Title/description length (limited only by system memory)
- ⚠️ Number of tasks (limited only by system memory)

### Constitutional Constraints
- ✅ No persistence (data lost on exit)
- ✅ In-memory only (no database/file system)
- ✅ Single entity (no relationships to other entities)

## Relationships

**None**. The Phase I Todo Application has only one entity (Task) with no relationships to other entities. Future phases may introduce:
- User entity (one-to-many: User → Tasks)
- Category entity (many-to-many: Tasks ↔ Categories)
- Tag entity (many-to-many: Tasks ↔ Tags)

These are out of scope for Phase I per the constitution.

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Create task | O(1) | O(1) |
| Read all tasks | O(n) | O(n) |
| Read task by ID | O(1) via dict lookup | O(1) |
| Update task by ID | O(1) via dict lookup | O(1) |
| Delete task by ID | O(n) for list removal, O(1) for dict | O(1) |
| Toggle completion | O(1) via dict lookup | O(1) |

**Expected performance**: All operations complete in < 1 second for up to 1000 tasks (per success criteria SC-002).

## Memory Usage Estimation

**Per Task**:
- id: 28 bytes (Python int object)
- title: ~50-100 bytes (average string)
- description: ~0-200 bytes (often None or short)
- completed: 28 bytes (Python bool object)
- Object overhead: ~56 bytes
- **Total per task**: ~200-400 bytes

**For 1000 tasks**: ~200-400 KB (well within constraints)

## References

1. Constitution Task Entity Rules: `.specify/memory/constitution.md` (lines 93-102)
2. Feature Specification: `specs/001-todo-app/spec.md`
3. Functional Requirements: FR-001 through FR-009
