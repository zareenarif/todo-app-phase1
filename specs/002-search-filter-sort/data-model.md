# Data Model: Search, Filter, and Sort

**Feature**: 002-search-filter-sort
**Date**: 2026-01-03
**Status**: Complete

## Overview

This feature does NOT introduce new persistent entities. It operates on the existing Task model with conceptual query criteria that exist only during method execution.

## Existing Entities (No Changes)

### Task

**Source**: `src/models/task.py` (unchanged from Phase I)

**Attributes**:
- `id` (int): Unique identifier, auto-incremented, immutable
- `title` (str): Task title, required, non-empty
- `description` (str|None): Optional task description
- `completed` (bool): Completion status, default False

**Validation Rules** (unchanged):
- Title must be non-empty after stripping whitespace
- ID is immutable (property-based implementation)
- Description may be None or empty string

**No modifications required** - search/filter/sort operations are read-only.

---

## Conceptual Entities (Runtime Only)

These entities exist only as method parameters and return values, not as persistent classes.

### SearchCriteria (Conceptual)

**Purpose**: Represents search parameters for keyword-based task discovery

**Attributes**:
- `keyword` (str): Search term to match against title and description
- `case_sensitive` (bool): Always False (case-insensitive by design)

**Behavior**:
- Empty or whitespace-only keyword matches all tasks
- Keyword must appear as substring in title OR description
- Matching is case-insensitive using `.lower()`

**Implementation**: Passed as string parameter to `search_tasks(keyword)` method

**Example Usage**:
```python
# User enters "buy"
results = service.search_tasks("buy")
# Matches: "Buy groceries", "buy books", "Need to BUY milk"
```

---

### FilterCriteria (Conceptual)

**Purpose**: Represents filtering parameters for status-based task visibility

**Attributes**:
- `status_filter` (str): One of 'all', 'pending', 'completed'

**Behavior**:
- 'all': Returns all tasks (no filtering)
- 'pending': Returns only tasks where completed=False
- 'completed': Returns only tasks where completed=True
- Invalid values default to 'all'

**Implementation**: Passed as string parameter to `filter_tasks(status_filter)` method

**Example Usage**:
```python
# User selects "Pending only"
results = service.filter_tasks("pending")
# Returns: All tasks where task.completed == False
```

---

### SortCriteria (Conceptual)

**Purpose**: Represents sorting parameters for task organization

**Attributes**:
- `sort_by` (str): One of 'id', 'title', 'status'
- `reverse` (bool): True for descending, False for ascending

**Behavior**:
- 'id': Sort by task.id (numerical)
- 'title': Sort by task.title (alphabetical, case-insensitive)
- 'status': Sort by task.completed (boolean: False < True)
- Invalid values return original order
- Stable sort preserves ID order for equal elements

**Implementation**: Passed as parameters to `sort_tasks(sort_by, reverse)` method

**Example Usage**:
```python
# User selects "Title (A-Z)"
results = service.sort_tasks("title", reverse=False)
# Returns: Tasks sorted alphabetically by title

# User selects "Status (completed first)"
results = service.sort_tasks("status", reverse=True)
# Returns: Completed tasks first, then pending
```

---

## Data Flow

### Search Operation

```
User Input: "buy"
    ↓
search_tasks(keyword="buy")
    ↓
[Filter] Iterate through self._tasks
    ↓
[Match] Check: "buy" in task.title.lower() OR "buy" in task.description.lower()
    ↓
[Return] List of matching Task objects (shallow copy)
    ↓
CLI displays results using existing table format
```

### Filter Operation

```
User Input: "Pending only" → "pending"
    ↓
filter_tasks(status_filter="pending")
    ↓
[Filter] Iterate through self._tasks
    ↓
[Match] Check: task.completed == False
    ↓
[Return] List of matching Task objects (shallow copy)
    ↓
CLI displays results using existing table format
```

### Sort Operation

```
User Input: "Title (A-Z)" → sort_by="title", reverse=False
    ↓
sort_tasks(sort_by="title", reverse=False)
    ↓
[Sort] Apply sorted() with key=lambda t: t.title.lower()
    ↓
[Return] New sorted list (shallow copy, non-destructive)
    ↓
CLI displays results using existing table format
```

### Combined Search + Filter

```
User Input: keyword="meeting", status="pending"
    ↓
search_and_filter(keyword="meeting", status_filter="pending")
    ↓
[Step 1] filter_tasks("pending") → subset of tasks
    ↓
[Step 2] Apply search on filtered subset
    ↓
[Return] List matching BOTH criteria
    ↓
CLI displays results using existing table format
```

---

## Storage Structure (Unchanged)

### TodoService Internal Storage

From Phase I implementation (no changes):

```python
class TodoService:
    def __init__(self):
        self._tasks = []          # List: maintains creation order
        self._task_dict = {}      # Dict: O(1) lookup by ID
        self._next_id = 1         # Counter: auto-increment
```

**Impact of Search/Filter/Sort**:
- Original `_tasks` list remains unchanged (non-destructive)
- All operations return NEW lists (shallow copies)
- `_task_dict` not used by search/filter/sort (iteration uses `_tasks`)
- No persistence - results exist only during display, then discarded

---

## Validation Rules

### Search Validation

| Input | Validation | Behavior |
|-------|------------|----------|
| Empty string "" | Valid | Returns all tasks |
| Whitespace "   " | Valid | Stripped, returns all tasks |
| Special chars "buy!" | Valid | Literal match (no regex) |
| Very long (>100 chars) | Valid | May not match anything |

### Filter Validation

| Input | Validation | Behavior |
|-------|------------|----------|
| "all" | Valid | Returns all tasks |
| "pending" | Valid | Returns incomplete tasks |
| "completed" | Valid | Returns complete tasks |
| Invalid value | Warning | Defaults to "all" |

### Sort Validation

| Input | Validation | Behavior |
|-------|------------|----------|
| "id" | Valid | Sort by ID (numeric) |
| "title" | Valid | Sort by title (alpha, case-insensitive) |
| "status" | Valid | Sort by completed (boolean) |
| Invalid value | Warning | Returns original order |
| reverse=True | Valid | Descending order |
| reverse=False | Valid | Ascending order (default) |

---

## State Transitions (None)

Search, filter, and sort operations are **stateless** and **non-destructive**:

- No state changes to Task objects
- No state changes to TodoService storage
- No persistent query state between operations
- Each operation returns fresh results
- User returns to main menu after each operation (no modal state)

**Constitutional Alignment**: Maintains simplicity - no state machines or complex transitions.

---

## Performance Characteristics

### Memory

| Operation | Additional Memory | Justification |
|-----------|-------------------|---------------|
| Search | O(n) for result list | Shallow copy of matching tasks |
| Filter | O(n) for result list | Shallow copy of matching tasks |
| Sort | O(n) for result list | New sorted list |
| Combined | O(n) for result list | Single result list |

**Worst case**: 1000 tasks × 8 bytes (pointer) = 8KB additional memory per operation

### Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Search | O(n × m) | n=tasks, m=avg text length (~150 chars) |
| Filter | O(n) | Single pass, boolean check |
| Sort by ID | O(n log n) | Timsort, numeric comparison |
| Sort by Title | O(n log n) | Timsort, string comparison |
| Sort by Status | O(n log n) | Timsort, boolean comparison |
| Search + Filter | O(n) | Two passes = O(2n) = O(n) |

**All operations meet <3 second requirement** for up to 1000 tasks.

---

## Edge Cases

### Empty Task List

- Search returns empty list with message "No tasks found"
- Filter returns empty list with appropriate message
- Sort returns empty list (no error)

### No Matches

- Search returns empty list with "No tasks found matching '[keyword]'"
- Filter returns empty list with "No [status] tasks found"
- Sort always succeeds (may return same order)

### Identical Values

- Sort by title with identical titles: Stable sort preserves ID order
- Sort by status: All pending have same value, stable sort preserves ID order

### Special Characters

- Search keyword with special chars: Literal match (no regex interpretation)
- Task title with Unicode: Python handles naturally (.lower() works)

---

## Integration Points

### With Existing Task Model

- **Read-only access**: No Task modifications
- **Attributes used**: id, title, description, completed
- **Methods used**: None (direct attribute access)

### With TodoService

- **New methods added** (to be implemented):
  - `search_tasks(keyword: str) -> list[Task]`
  - `filter_tasks(status_filter: str) -> list[Task]`
  - `sort_tasks(sort_by: str, reverse: bool = False) -> list[Task]`
  - `search_and_filter(keyword: str | None, status_filter: str) -> list[Task]`

- **Existing methods unchanged**:
  - `add_task()`, `get_all_tasks()`, `get_task_by_id()`, etc.

### With CLI Layer

- **Input**: User provides keyword/filter/sort criteria via prompts
- **Output**: Results displayed using existing table format from `handle_view_tasks()`
- **Reuse**: Same display logic, same error handling patterns

---

## Summary

**No new persistent entities** - this feature is purely operational, working with existing Task model.

**Conceptual entities** (SearchCriteria, FilterCriteria, SortCriteria) exist only as method parameters.

**All operations are**:
- ✅ Non-destructive (original list preserved)
- ✅ Stateless (no persistent query state)
- ✅ Efficient (O(n) or O(n log n))
- ✅ Constitutional (standard library only, in-memory)

**Ready for contracts phase** - CLI interface specifications next.
