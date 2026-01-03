# Quickstart: Implementing Search, Filter, and Sort

**Feature**: 002-search-filter-sort
**Target Audience**: Developers implementing this feature
**Estimated Time**: 3-4 hours for complete implementation

## Prerequisites

- ✅ Phase I Todo Application fully implemented and functional
- ✅ Familiarity with `src/services/todo_service.py` and `src/cli/menu.py`
- ✅ Python 3.13+ environment ready
- ✅ All planning documents read (spec.md, plan.md, research.md, data-model.md, contracts/cli-interface.md)

---

## Implementation Overview

**Total Work**: 3 new service methods + 3 new CLI handlers + menu updates

**Files to Modify**:
1. `src/services/todo_service.py` - Add 4 new methods
2. `src/cli/menu.py` - Add 3 new handlers, update 3 existing functions

**Files Unchanged**:
- `src/models/task.py` - No changes
- `main.py` - No changes

**Estimated Effort**:
- Service layer: ~1 hour (4 methods)
- CLI handlers: ~1.5 hours (3 handlers + 2 validators)
- Menu integration: ~30 minutes (update display, validation, routing)
- Polish & testing: ~1 hour (docstrings, manual testing)

---

## Step-by-Step Implementation

### Step 1: Service Layer Methods (src/services/todo_service.py)

**Add these 4 methods to the TodoService class:**

#### Method 1: search_tasks()

```python
def search_tasks(self, keyword):
    """
    Search tasks by keyword in title or description.

    Args:
        keyword (str): Search term (case-insensitive)

    Returns:
        list: Tasks matching keyword in title or description
    """
    if not keyword or not keyword.strip():
        return self._tasks.copy()

    keyword_lower = keyword.lower().strip()
    results = [
        task for task in self._tasks
        if keyword_lower in task.title.lower() or
           (task.description and keyword_lower in task.description.lower())
    ]
    return results
```

**Test**:
```python
# Manually test after implementation:
# 1. Add tasks with titles: "Buy groceries", "Buy books", "Read email"
# 2. search_tasks("buy") should return first two tasks
# 3. search_tasks("") should return all tasks
```

#### Method 2: filter_tasks()

```python
def filter_tasks(self, status_filter):
    """
    Filter tasks by completion status.

    Args:
        status_filter (str): 'all', 'pending', or 'completed'

    Returns:
        list: Filtered task list
    """
    if status_filter == 'all':
        return self._tasks.copy()
    elif status_filter == 'pending':
        return [task for task in self._tasks if not task.completed]
    elif status_filter == 'completed':
        return [task for task in self._tasks if task.completed]
    else:
        return self._tasks.copy()  # Invalid filter returns all
```

**Test**:
```python
# 1. Add 3 pending tasks and 2 completed tasks
# 2. filter_tasks("pending") should return 3 tasks
# 3. filter_tasks("completed") should return 2 tasks
# 4. filter_tasks("all") should return all 5 tasks
```

#### Method 3: sort_tasks()

```python
def sort_tasks(self, sort_by, reverse=False):
    """
    Sort tasks by specified criterion.

    Args:
        sort_by (str): 'id', 'title', or 'status'
        reverse (bool): True for descending, False for ascending

    Returns:
        list: Sorted task list
    """
    if sort_by == 'id':
        return sorted(self._tasks, key=lambda t: t.id, reverse=reverse)
    elif sort_by == 'title':
        return sorted(self._tasks, key=lambda t: t.title.lower(), reverse=reverse)
    elif sort_by == 'status':
        return sorted(self._tasks, key=lambda t: t.completed, reverse=reverse)
    else:
        return self._tasks.copy()  # Invalid sort returns original order
```

**Test**:
```python
# 1. Add tasks with IDs 1, 3, 5, 2, 4 (after deletions/adds)
# 2. sort_tasks("id", False) should return: 1, 2, 3, 4, 5
# 3. sort_tasks("title", False) should return alphabetical order
# 4. sort_tasks("status", True) should return completed first
```

#### Method 4: search_and_filter()

```python
def search_and_filter(self, keyword=None, status_filter='all'):
    """
    Combine search and filter operations.

    Args:
        keyword (str, optional): Search keyword
        status_filter (str): 'all', 'pending', or 'completed'

    Returns:
        list: Tasks matching both criteria
    """
    # Filter first (typically smaller result set)
    filtered = self.filter_tasks(status_filter)

    # Then search within filtered results
    if not keyword or not keyword.strip():
        return filtered

    keyword_lower = keyword.lower().strip()
    results = [
        task for task in filtered
        if keyword_lower in task.title.lower() or
           (task.description and keyword_lower in task.description.lower())
    ]
    return results
```

**Test**:
```python
# 1. Add "Buy groceries" (pending), "Buy books" (completed), "Read email" (pending)
# 2. search_and_filter("buy", "pending") should return only "Buy groceries"
# 3. search_and_filter("buy", "all") should return "Buy groceries" and "Buy books"
```

**✓ Checkpoint**: All 4 service methods implemented and manually tested

---

### Step 2: CLI Validation Helpers (src/cli/menu.py)

**Add these 2 validation helper functions:**

#### Helper 1: get_filter_choice()

```python
def get_filter_choice():
    """
    Get and validate filter choice from user.

    Returns:
        str: 'all', 'pending', or 'completed'
    """
    print("Filter by status:")
    print("  1. All tasks")
    print("  2. Pending only")
    print("  3. Completed only")

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

#### Helper 2: get_sort_choice()

```python
def get_sort_choice():
    """
    Get and validate sort choice from user.

    Returns:
        tuple: (sort_by: str, reverse: bool)
    """
    print("Sort by:")
    print("  1. ID (ascending)")
    print("  2. ID (descending)")
    print("  3. Title (A-Z)")
    print("  4. Title (Z-A)")
    print("  5. Status (completed first)")
    print("  6. Status (pending first)")

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

### Step 3: CLI Handlers (src/cli/menu.py)

**Add these 3 handler functions:**

#### Handler 1: handle_search_filter_tasks()

```python
def handle_search_filter_tasks(service):
    """
    Handle searching and filtering tasks.

    Args:
        service (TodoService): Todo service instance
    """
    print("\n" + "=" * 30)
    print("=== Search/Filter Tasks ===")
    print("=" * 30)
    print()

    # Get search keyword
    keyword = input("Enter keyword to search (or press Enter to skip): ").strip()
    if not keyword:
        keyword = None

    # Get filter choice
    status_filter = get_filter_choice()

    # Execute combined search and filter
    results = service.search_and_filter(keyword, status_filter)

    # Display results
    if not results:
        if keyword and status_filter != 'all':
            print(f"\nNo tasks found matching '{keyword}' ({status_filter} only).")
        elif keyword:
            print(f"\nNo tasks found matching '{keyword}'.")
        elif status_filter == 'pending':
            print("\nNo pending tasks found.")
        elif status_filter == 'completed':
            print("\nNo completed tasks found.")
        else:
            print("\nNo tasks found. Add a task to get started!")
        return

    # Display header based on what was applied
    if keyword and status_filter != 'all':
        print(f"\nFound {len(results)} task{'s' if len(results) != 1 else ''} matching '{keyword}' ({status_filter} only):\n")
    elif keyword:
        print(f"\nFound {len(results)} task{'s' if len(results) != 1 else ''} matching '{keyword}':\n")
    elif status_filter == 'pending':
        print(f"\nShowing {len(results)} pending task{'s' if len(results) != 1 else ''}:\n")
    elif status_filter == 'completed':
        print(f"\nShowing {len(results)} completed task{'s' if len(results) != 1 else ''}:\n")
    else:
        print(f"\nShowing all {len(results)} task{'s' if len(results) != 1 else ''}:\n")

    # Display table (reuse existing format from handle_view_tasks)
    print(f"{'ID':<5} | {'Title':<30} | {'Status'}")
    print("-" * 50)

    for task in results:
        status = "Completed" if task.completed else "Pending"
        title_display = task.title[:30] if len(task.title) > 30 else task.title
        print(f"{task.id:<5} | {title_display:<30} | {status}")

    print(f"\nTotal: {len(results)} task{'s' if len(results) != 1 else ''}")
```

#### Handler 2: handle_sort_tasks()

```python
def handle_sort_tasks(service):
    """
    Handle sorting tasks.

    Args:
        service (TodoService): Todo service instance
    """
    print("\n" + "=" * 30)
    print("===    Sort Tasks    ===")
    print("=" * 30)
    print()

    # Get sort choice
    sort_by, reverse = get_sort_choice()

    # Execute sort
    if sort_by is None:
        results = service.get_all_tasks()
    else:
        results = service.sort_tasks(sort_by, reverse)

    # Display results
    if not results:
        print("\nNo tasks found. Add a task to get started!")
        return

    # Display header based on sort criteria
    if sort_by == "id":
        direction = "descending" if reverse else "ascending"
        print(f"\nTasks sorted by ID ({direction}):\n")
    elif sort_by == "title":
        direction = "Z-A" if reverse else "A-Z"
        print(f"\nTasks sorted by Title ({direction}):\n")
    elif sort_by == "status":
        direction = "completed first" if reverse else "pending first"
        print(f"\nTasks sorted by Status ({direction}):\n")
    else:
        print("\nShowing tasks in original order:\n")

    # Display table
    print(f"{'ID':<5} | {'Title':<30} | {'Status'}")
    print("-" * 50)

    for task in results:
        status = "Completed" if task.completed else "Pending"
        title_display = task.title[:30] if len(task.title) > 30 else task.title
        print(f"{task.id:<5} | {title_display:<30} | {status}")

    print(f"\nTotal: {len(results)} task{'s' if len(results) != 1 else ''}")
```

**✓ Checkpoint**: All handlers implemented

---

### Step 4: Update Menu Display (src/cli/menu.py)

**Modify `display_menu()` function:**

```python
def display_menu():
    """Display the main menu with numbered options."""
    print("\n" + "=" * 30)
    print("===  Todo Application  ===")
    print("=" * 30)
    print("\n1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Search/Filter Tasks")       # NEW
    print("7. Sort Tasks")                 # NEW
    print("8. Exit")                       # MOVED from 6
    print()
```

---

### Step 5: Update Menu Validation (src/cli/menu.py)

**Modify `get_menu_choice()` function:**

```python
def get_menu_choice():
    """
    Get and validate user menu choice.

    Returns:
        int or None: Valid choice (1-8) or None if invalid
    """
    try:
        choice = input("Enter your choice (1-8): ").strip()  # Changed from 1-6
        choice_num = int(choice)
        if 1 <= choice_num <= 8:  # Changed from 1-6
            return choice_num
        else:
            print("\n✗ Error: Invalid choice. Please enter a number between 1 and 8.")  # Updated message
            return None
    except ValueError:
        print("\n✗ Error: Invalid choice. Please enter a number between 1 and 8.")  # Updated message
        return None
```

---

### Step 6: Update Menu Routing (src/cli/menu.py)

**Modify `run_menu()` function:**

```python
def run_menu():
    """
    Run the main application menu loop.

    Initializes the service and continuously displays menu until user exits.
    """
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
        elif choice == 8:                         # MOVED from 6
            exit_requested = handle_exit()
```

**✓ Checkpoint**: All menu updates complete

---

## Manual Testing Checklist

### Test 1: Search Functionality

- [ ] Add tasks: "Buy groceries", "Buy books", "Read email"
- [ ] Select option 6
- [ ] Search for "buy"
- [ ] Select "All tasks" filter
- [ ] Expected: See "Buy groceries" and "Buy books"
- [ ] Search for "xyz" (no matches)
- [ ] Expected: See "No tasks found matching 'xyz'"

### Test 2: Filter Functionality

- [ ] Add 3 pending and 2 completed tasks
- [ ] Select option 6
- [ ] Press Enter (skip search)
- [ ] Select "Pending only" filter
- [ ] Expected: See 3 pending tasks only
- [ ] Repeat with "Completed only" filter
- [ ] Expected: See 2 completed tasks only

### Test 3: Sort Functionality

- [ ] Add tasks: "Zebra", "Apple", "Mango"
- [ ] Select option 7
- [ ] Choose "Title (A-Z)"
- [ ] Expected: See Apple, Mango, Zebra
- [ ] Select option 7 again
- [ ] Choose "Title (Z-A)"
- [ ] Expected: See Zebra, Mango, Apple

### Test 4: Combined Search + Filter

- [ ] Add "Buy groceries" (pending), "Buy books" (completed)
- [ ] Select option 6
- [ ] Search for "buy"
- [ ] Select "Pending only" filter
- [ ] Expected: See only "Buy groceries"

### Test 5: Edge Cases

- [ ] Empty task list: Search/filter/sort should show "No tasks found"
- [ ] Invalid filter choice: Should default to "All" with error message
- [ ] Invalid sort choice: Should show original order with error message
- [ ] Empty search keyword: Should show all tasks (filtered by status if applicable)

**✓ All tests passing**: Feature is complete!

---

## Common Issues and Solutions

### Issue 1: Menu validation not updated

**Symptom**: Menu accepts choices 1-6 but rejects 7-8

**Solution**: Check `get_menu_choice()` - ensure range is 1-8, not 1-6

### Issue 2: Search not case-insensitive

**Symptom**: Searching for "buy" doesn't match "Buy"

**Solution**: Ensure both keyword and task fields use `.lower()` for comparison

### Issue 3: Sort modifies original list

**Symptom**: Subsequent "View Tasks" shows sorted order

**Solution**: Ensure `sort_tasks()` uses `sorted()` (creates new list), not `list.sort()` (in-place)

### Issue 4: Filter returns None for invalid input

**Symptom**: Crash when invalid filter choice entered

**Solution**: Ensure `get_filter_choice()` returns "all" for invalid input, not None

---

## Performance Validation

Run these tests to ensure performance requirements are met:

1. **Large Task List**: Add 100+ tasks, perform search/filter/sort
   - Expected: All operations complete in <1 second

2. **Long Titles**: Add tasks with 200+ character titles
   - Expected: Table displays truncated titles correctly

3. **Special Characters**: Search for keywords with special chars (!, @, #)
   - Expected: Literal match (no regex errors)

---

## Completion Checklist

- [ ] All 4 service methods implemented in `todo_service.py`
- [ ] All 2 validation helpers implemented in `menu.py`
- [ ] All 3 handlers implemented in `menu.py`
- [ ] `display_menu()` updated with options 6, 7, 8
- [ ] `get_menu_choice()` updated to validate 1-8
- [ ] `run_menu()` updated with new routing
- [ ] All docstrings added to new methods
- [ ] Manual testing complete (all 5 test scenarios pass)
- [ ] Edge cases validated
- [ ] Performance validated (large lists)
- [ ] Code reviewed for simplicity and readability
- [ ] README.md updated (optional)

---

## Next Steps After Implementation

1. ✅ Mark all tasks complete in `tasks.md`
2. Run application: `python main.py`
3. Perform full acceptance testing against spec.md scenarios
4. Create PHR (Prompt History Record) for green stage
5. Consider git commit (optional)

---

**Implementation Status**: Ready to begin
**Estimated Completion**: 3-4 hours from start to finish
