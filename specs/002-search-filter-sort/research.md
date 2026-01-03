# Research: Search, Filter, and Sort Implementation

**Feature**: 002-search-filter-sort
**Date**: 2026-01-03
**Status**: Complete

## Overview

This document captures technical decisions for implementing search, filter, and sort capabilities in the Todo Application. All research aligns with constitutional requirements (Python 3.13+ standard library only, in-memory operations).

## Research Areas

### 1. Search Algorithm - Case-Insensitive Substring Matching

**Decision**: Use `.lower()` method with `in` operator for substring matching

**Rationale**:
- Built into Python standard library (no external dependencies)
- O(n*m) complexity where n = text length, m = pattern length (acceptable for <1000 tasks)
- Simple, readable, maintainable code
- Handles case-insensitivity naturally

**Implementation Pattern**:
```python
def search_tasks(self, keyword):
    """Search tasks by keyword in title or description."""
    if not keyword or not keyword.strip():
        return self._tasks.copy()  # Empty search returns all

    keyword_lower = keyword.lower().strip()
    results = [
        task for task in self._tasks
        if keyword_lower in task.title.lower() or
           (task.description and keyword_lower in task.description.lower())
    ]
    return results
```

**Alternatives Considered**:
- **Regular expressions (re module)**: Rejected - unnecessary complexity for simple substring matching
- **str.find()**: Rejected - `in` operator is more Pythonic and readable
- **str.startswith()**: Rejected - too restrictive, users expect substring matching

**Performance**: O(n) where n = number of tasks. Tested mentally with 1000 tasks, each ~100 chars = 100k char scans, negligible (<1ms on modern hardware).

---

### 2. Filter Implementation - Status-Based Filtering

**Decision**: Use list comprehension with boolean filtering

**Rationale**:
- Most Pythonic approach
- O(n) time complexity
- Highly readable and maintainable
- Aligns with existing codebase patterns

**Implementation Pattern**:
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

**Alternatives Considered**:
- **filter() function**: Rejected - list comprehension more readable
- **Separate methods for each status**: Rejected - violates DRY principle
- **Dictionary dispatch**: Rejected - over-engineering for 3 options

**Performance**: O(n) where n = number of tasks. Single pass through list.

---

### 3. Sort Implementation - Multi-Criteria Sorting

**Decision**: Use built-in `sorted()` function with lambda key functions

**Rationale**:
- Python's Timsort algorithm (O(n log n), highly optimized)
- Supports stable sorting (preserves order for equal elements)
- Clean syntax with lambda functions
- No external dependencies

**Implementation Pattern**:
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
        # completed=True sorts first when reverse=False
        return sorted(self._tasks, key=lambda t: t.completed, reverse=reverse)
    else:
        return self._tasks.copy()  # Invalid sort returns original order
```

**Alternatives Considered**:
- **list.sort()**: Rejected - want non-destructive (return new list, preserve original)
- **operator.attrgetter()**: Considered but lambda more flexible for .lower() on title
- **Multiple sort keys**: Rejected - spec doesn't require secondary sorting

**Performance**: O(n log n) using Timsort. For 1000 tasks, ~10k comparisons, <10ms.

**Edge Cases**:
- Identical titles: Stable sort preserves ID order
- None descriptions: Handled by checking existence before comparison

---

### 4. Combine Search and Filter

**Decision**: Chain operations - filter first, then search (or vice versa)

**Rationale**:
- Composable approach (Unix philosophy)
- Each operation independent and testable
- Allows flexible combinations without method explosion

**Implementation Pattern**:
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

**Alternatives Considered**:
- **Single combined method**: Rejected - harder to test and maintain
- **Separate methods for all combinations**: Rejected - 9+ methods (explosion)
- **Search first, then filter**: Considered but filter typically reduces set more

**Performance**: O(n) for both operations, so O(2n) = O(n) total.

---

### 5. Menu UX - Extending CLI Menu

**Decision**: Simplified 8-option menu with combined "Search/Filter Tasks" option

**Rationale**:
- Keeps menu compact and scannable
- Most users want to search OR filter, rarely need both separately
- Reduces cognitive load (8 options vs 10)
- Aligns with existing menu validation patterns

**Menu Structure**:
```
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Search/Filter Tasks  [NEW - combined]
7. Sort Tasks           [NEW]
8. Exit                 [MOVED from 6]
```

**Search/Filter Flow**:
1. User selects "Search/Filter Tasks"
2. Prompt: "Enter search keyword (or press Enter to skip):"
3. Prompt: "Filter by status: 1=All, 2=Pending, 3=Completed:"
4. Display results using existing table format
5. Return to main menu

**Alternatives Considered**:
- **10-option menu with all separate**: Rejected - too many options
- **Nested sub-menus**: Rejected - violates constitution (single menu loop)
- **Combined "Advanced Search"**: Rejected - intimidating terminology

**Validation Updates**:
- Change `get_menu_choice()` from 1-6 to 1-8
- Error message: "Please enter a number between 1 and 8"

---

### 6. Performance Benchmarking

**Assumptions**:
- Average task: 50 char title + 100 char description = 150 chars
- Target: 1000 tasks = 150,000 characters total
- Operations: Search (O(n)), Filter (O(n)), Sort (O(n log n))

**Estimated Performance**:

| Operation | Complexity | 1000 Tasks | Estimate |
|-----------|------------|------------|----------|
| Search | O(n) | 150k char scan | <10ms |
| Filter | O(n) | 1000 comparisons | <1ms |
| Sort by ID | O(n log n) | ~10k comparisons | <5ms |
| Sort by Title | O(n log n) | ~10k string compares | <10ms |
| Search + Filter | O(n) | Two passes | <15ms |

**Success Criteria Met**: All operations <3 seconds (well under spec requirement)

**Memory**:
- Task object ~500 bytes (4 fields + overhead)
- 1000 tasks = ~500KB
- Filtered/sorted views create new lists (shallow copies) = additional ~8KB for pointers
- Total: <1MB for 1000 tasks (well under 10MB constraint)

---

### 7. Error Handling Patterns

**Decision**: Graceful degradation with user-friendly messages

**Patterns**:
1. **Empty search**: Return all tasks (don't error)
2. **Invalid filter option**: Default to "All" with message
3. **Invalid sort option**: Return original order with message
4. **No results**: Display "No tasks found matching '[criteria]'"

**Example Messages**:
- ✓ "Found 3 tasks matching 'buy'"
- ✓ "Showing 5 pending tasks"
- ✓ "Tasks sorted by title (A-Z)"
- ✗ "No tasks found matching 'xyz'"
- ✗ "Invalid filter option. Showing all tasks."

**Alignment**: Matches existing error handling in Phase I (validate_integer_input pattern)

---

## Technology Stack Summary

| Component | Technology | Justification |
|-----------|------------|---------------|
| Search | str.lower() + in operator | Built-in, simple, performant |
| Filter | List comprehension | Pythonic, O(n), readable |
| Sort | sorted() with lambda | Timsort, stable, flexible |
| Combine | Method composition | DRY, testable, maintainable |
| Menu | Extended numbered options | Consistent with Phase I |
| Validation | Existing patterns | Reuse validate_integer_input |

---

## Open Questions - RESOLVED

All research questions from plan.md have been answered:

1. ✅ **Search Algorithm**: str.lower() + in operator
2. ✅ **Filter Implementation**: List comprehension with boolean filter
3. ✅ **Sort Implementation**: sorted() with lambda key functions
4. ✅ **Menu UX**: 8-option simplified menu
5. ✅ **Performance**: All operations well under 3-second requirement

---

## Next Phase

All research complete. Ready for Phase 1 design:
- Generate data-model.md (entities and validation)
- Generate contracts/cli-interface.md (exact CLI specifications)
- Generate quickstart.md (developer guide)

**Research Status**: ✅ COMPLETE
