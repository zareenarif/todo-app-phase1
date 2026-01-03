# CLI Interface Contract: Search, Filter, and Sort

**Feature**: 002-search-filter-sort
**Date**: 2026-01-03
**Status**: Complete

## Overview

This document specifies the exact CLI behavior for search, filter, and sort operations. All specifications are binding for implementation.

---

## Updated Main Menu

### Menu Display

```
==============================
===  Todo Application  ===
==============================

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Search/Filter Tasks
7. Sort Tasks
8. Exit

Enter your choice (1-8): _
```

**Changes from Phase I**:
- Added option 6: "Search/Filter Tasks" (new)
- Added option 7: "Sort Tasks" (new)
- Moved "Exit" from position 6 to position 8

**Validation**:
- Input range: 1-8 (updated from 1-6)
- Error message: "✗ Error: Invalid choice. Please enter a number between 1 and 8."

---

## Option 6: Search/Filter Tasks

### Flow Diagram

```
Main Menu → Select 6
    ↓
Display "Search/Filter Tasks" header
    ↓
Prompt: "Enter keyword to search (or press Enter to skip):"
    ↓
[User enters keyword or presses Enter]
    ↓
Prompt: "Filter by status:\n  1. All tasks\n  2. Pending only\n  3. Completed only\nEnter choice (1-3):"
    ↓
[User enters 1, 2, or 3]
    ↓
Execute search_and_filter(keyword, status_filter)
    ↓
Display results in table format
    ↓
Return to main menu
```

### Exact Prompts and Responses

#### Header

```
==============================
=== Search/Filter Tasks ===
==============================
```

#### Search Prompt

```
Enter keyword to search (or press Enter to skip): _
```

**User Input Handling**:
- Empty input (just Enter): `keyword = None` → no search filtering
- Whitespace only: Stripped, treated as empty → no search filtering
- Any text: `keyword = user_input.strip()`

#### Filter Prompt

```
Filter by status:
  1. All tasks
  2. Pending only
  3. Completed only
Enter choice (1-3): _
```

**User Input Handling**:
- 1 → `status_filter = "all"`
- 2 → `status_filter = "pending"`
- 3 → `status_filter = "completed"`
- Invalid input → Display error, default to "all"

**Error for Invalid Filter**:
```
✗ Error: Invalid choice. Showing all tasks.
```

#### Results Display - With Matches

**Example 1: Search only (no filter)**
```
Found 3 tasks matching 'buy':

ID    | Title                          | Status
--------------------------------------------------
1     | Buy groceries                  | Pending
2     | Buy books                      | Completed
5     | Need to buy milk               | Pending

Total: 3 tasks
```

**Example 2: Filter only (no search)**
```
Showing 5 pending tasks:

ID    | Title                          | Status
--------------------------------------------------
1     | Buy groceries                  | Pending
3     | Read email                     | Pending
5     | Need to buy milk               | Pending
7     | Call mom                       | Pending
9     | Finish report                  | Pending

Total: 5 tasks
```

**Example 3: Search AND filter**
```
Found 1 task matching 'buy' (pending only):

ID    | Title                          | Status
--------------------------------------------------
1     | Buy groceries                  | Pending

Total: 1 task
```

#### Results Display - No Matches

**No search results**:
```
No tasks found matching 'xyz'.
```

**No filtered results**:
```
No pending tasks found.
```
or
```
No completed tasks found.
```

**No results for combined search + filter**:
```
No tasks found matching 'meeting' (pending only).
```

#### Results Display - Empty Task List

```
No tasks found. Add a task to get started!
```

---

## Option 7: Sort Tasks

### Flow Diagram

```
Main Menu → Select 7
    ↓
Display "Sort Tasks" header
    ↓
Prompt: "Sort by:\n  1. ID (ascending)\n  2. ID (descending)\n  3. Title (A-Z)\n  4. Title (Z-A)\n  5. Status (completed first)\n  6. Status (pending first)\nEnter choice (1-6):"
    ↓
[User enters 1-6]
    ↓
Execute sort_tasks(sort_by, reverse)
    ↓
Display sorted results in table format
    ↓
Return to main menu
```

### Exact Prompts and Responses

#### Header

```
==============================
===    Sort Tasks    ===
==============================
```

#### Sort Prompt

```
Sort by:
  1. ID (ascending)
  2. ID (descending)
  3. Title (A-Z)
  4. Title (Z-A)
  5. Status (completed first)
  6. Status (pending first)
Enter choice (1-6): _
```

**User Input Handling**:
- 1 → `sort_tasks(sort_by="id", reverse=False)`
- 2 → `sort_tasks(sort_by="id", reverse=True)`
- 3 → `sort_tasks(sort_by="title", reverse=False)`
- 4 → `sort_tasks(sort_by="title", reverse=True)`
- 5 → `sort_tasks(sort_by="status", reverse=True)`  # completed=True > completed=False
- 6 → `sort_tasks(sort_by="status", reverse=False)` # completed=False < completed=True
- Invalid → Display error, show original order

**Error for Invalid Sort**:
```
✗ Error: Invalid sort option. Showing tasks in original order.
```

#### Results Display - Sorted

**Example 1: Sort by ID ascending**
```
Tasks sorted by ID (ascending):

ID    | Title                          | Status
--------------------------------------------------
1     | Buy groceries                  | Pending
2     | Call mom                       | Completed
3     | Read email                     | Pending
4     | Finish report                  | Completed
5     | Buy books                      | Pending

Total: 5 tasks
```

**Example 2: Sort by Title (A-Z)**
```
Tasks sorted by Title (A-Z):

ID    | Title                          | Status
--------------------------------------------------
5     | Buy books                      | Pending
1     | Buy groceries                  | Pending
2     | Call mom                       | Completed
4     | Finish report                  | Completed
3     | Read email                     | Pending

Total: 5 tasks
```

**Example 3: Sort by Status (completed first)**
```
Tasks sorted by Status (completed first):

ID    | Title                          | Status
--------------------------------------------------
2     | Call mom                       | Completed
4     | Finish report                  | Completed
1     | Buy groceries                  | Pending
3     | Read email                     | Pending
5     | Buy books                      | Pending

Total: 5 tasks
```

#### Results Display - Empty Task List

```
No tasks found. Add a task to get started!
```

---

## Table Format Specification

### Standard Table Layout

**Consistent with Phase I `handle_view_tasks()`**:

```
ID    | Title                          | Status
--------------------------------------------------
{id:<5} | {title:<30} | {status}
```

**Field Specifications**:
- **ID**: Left-aligned, 5 character width, no padding
- **Title**: Left-aligned, 30 character width, truncated if longer
- **Status**: "Pending" or "Completed", no width constraint
- **Separator**: 50 hyphens

**Title Truncation**:
- If `len(title) > 30`: Display first 30 characters only
- No ellipsis (...) appended (matches Phase I behavior)

**Total Count**:
- Format: `"Total: {count} task{'s' if count != 1 else ''}"`
- Examples:
  - `Total: 1 task`
  - `Total: 5 tasks`
  - `Total: 0 tasks` (for empty results)

---

## Input Validation Patterns

### Menu Choice Validation

**Function**: `get_menu_choice()`

**Updated Logic**:
```python
try:
    choice = input("Enter your choice (1-8): ").strip()
    choice_num = int(choice)
    if 1 <= choice_num <= 8:  # Changed from 1-6
        return choice_num
    else:
        print("\n✗ Error: Invalid choice. Please enter a number between 1 and 8.")
        return None
except ValueError:
    print("\n✗ Error: Invalid choice. Please enter a number between 1 and 8.")
    return None
```

### Filter Choice Validation

**New Function**: `get_filter_choice()`

```python
try:
    choice = input("Enter choice (1-3): ").strip()
    choice_num = int(choice)
    if choice_num == 1:
        return "all"
    elif choice_num == 2:
        return "pending"
    elif choice_num == 3:
        return "completed"
    else:
        print("\n✗ Error: Invalid choice. Showing all tasks.")
        return "all"
except ValueError:
    print("\n✗ Error: Invalid choice. Showing all tasks.")
    return "all"
```

### Sort Choice Validation

**New Function**: `get_sort_choice()`

```python
try:
    choice = input("Enter choice (1-6): ").strip()
    choice_num = int(choice)
    if choice_num == 1:
        return ("id", False)
    elif choice_num == 2:
        return ("id", True)
    elif choice_num == 3:
        return ("title", False)
    elif choice_num == 4:
        return ("title", True)
    elif choice_num == 5:
        return ("status", True)
    elif choice_num == 6:
        return ("status", False)
    else:
        print("\n✗ Error: Invalid sort option. Showing tasks in original order.")
        return (None, False)
except ValueError:
    print("\n✗ Error: Invalid sort option. Showing tasks in original order.")
    return (None, False)
```

---

## Error Handling

### Error Message Format

**Consistent with Phase I**:
- Error prefix: `✗` (multiplication symbol)
- Success prefix: `✓` (checkmark)
- Format: `"\n✗ Error: {message}"`

### Error Scenarios

| Scenario | Error Message | Behavior |
|----------|---------------|----------|
| Invalid menu choice (not 1-8) | "✗ Error: Invalid choice. Please enter a number between 1 and 8." | Re-prompt menu |
| Invalid filter choice | "✗ Error: Invalid choice. Showing all tasks." | Default to "all" |
| Invalid sort choice | "✗ Error: Invalid sort option. Showing tasks in original order." | Show unsorted |
| Non-numeric menu input | "✗ Error: Invalid choice. Please enter a number between 1 and 8." | Re-prompt menu |
| Non-numeric filter input | "✗ Error: Invalid choice. Showing all tasks." | Default to "all" |
| Non-numeric sort input | "✗ Error: Invalid sort option. Showing tasks in original order." | Show unsorted |

### No Errors (Valid Behaviors)

- Empty search keyword → Show all tasks (filtered by status if applicable)
- Empty task list → Show "No tasks found" message, no error
- No search results → Show "No tasks found matching '[keyword]'" message, no error

---

## Integration with Existing Menu

### Updated `run_menu()` Logic

```python
def run_menu():
    service = TodoService()
    exit_requested = False

    while not exit_requested:
        display_menu()
        choice = get_menu_choice()

        if choice is None:
            continue

        if choice == 1:
            handle_add_task(service)
        elif choice == 2:
            handle_view_tasks(service)
        elif choice == 3:
            handle_update_task(service)
        elif choice == 4:
            handle_delete_task(service)
        elif choice == 5:
            handle_toggle_completion(service)
        elif choice == 6:
            handle_search_filter_tasks(service)  # NEW
        elif choice == 7:
            handle_sort_tasks(service)           # NEW
        elif choice == 8:
            exit_requested = handle_exit()       # MOVED from 6
```

---

## Acceptance Testing Examples

### Test Case 1: Search Only

**Actions**:
1. Add tasks: "Buy groceries", "Buy books", "Read email"
2. Select option 6
3. Enter keyword: "buy"
4. Select filter: 1 (All tasks)

**Expected Output**:
```
Found 2 tasks matching 'buy':

ID    | Title                          | Status
--------------------------------------------------
1     | Buy groceries                  | Pending
2     | Buy books                      | Pending

Total: 2 tasks
```

### Test Case 2: Filter Only

**Actions**:
1. Have 3 pending and 2 completed tasks
2. Select option 6
3. Press Enter (skip search)
4. Select filter: 2 (Pending only)

**Expected Output**:
```
Showing 3 pending tasks:

ID    | Title                          | Status
--------------------------------------------------
1     | Buy groceries                  | Pending
3     | Read email                     | Pending
5     | Call mom                       | Pending

Total: 3 tasks
```

### Test Case 3: Sort by Title

**Actions**:
1. Have tasks: "Zebra", "Apple", "Mango"
2. Select option 7
3. Select sort: 3 (Title A-Z)

**Expected Output**:
```
Tasks sorted by Title (A-Z):

ID    | Title                          | Status
--------------------------------------------------
2     | Apple                          | Pending
3     | Mango                          | Pending
1     | Zebra                          | Pending

Total: 3 tasks
```

---

## Performance Requirements

**All operations must complete within 3 seconds** for task lists up to 1000 tasks.

**Display requirements**:
- Results appear immediately after selection (no loading spinner)
- No pagination (display all results in single table)
- Table format consistent with Phase I

---

## Summary

**CLI Changes**:
- ✅ Menu extended from 6 to 8 options
- ✅ 2 new handlers: `handle_search_filter_tasks()`, `handle_sort_tasks()`
- ✅ 2 new validation helpers: `get_filter_choice()`, `get_sort_choice()`
- ✅ Updated menu validation: 1-8 instead of 1-6
- ✅ All error messages follow existing patterns
- ✅ All table displays reuse existing format

**Ready for implementation** - all CLI specifications complete and testable.
