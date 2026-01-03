# Research: Phase I Todo Application

**Feature**: 001-todo-app
**Date**: 2026-01-03
**Status**: Complete

## Executive Summary

All technical decisions for Phase I Todo Application are fully specified by the project constitution. No research was required as all choices are predetermined and non-negotiable per constitutional principles.

## Technology Stack

### Decision: Python 3.13+
**Rationale**: Mandated by constitution's Technical Constraints
**Alternatives considered**: None (constitutional requirement)
**References**: `.specify/memory/constitution.md` - Technical Constraints section

### Decision: Python Standard Library Only
**Rationale**: Constitution Principle IV (Simplicity Over Complexity) mandates no external dependencies
**Alternatives considered**: None (constitutional requirement)
**Impact**: All functionality must be implemented using built-in Python modules

## Data Storage

### Decision: In-Memory (Lists and Dictionaries)
**Rationale**: Constitution explicitly prohibits databases and file system persistence for Phase I
**Alternatives considered**: None (constitutional prohibition)
**Implementation approach**:
- Task storage: Python list to maintain order
- Task lookup: Dictionary mapping ID to task for O(1) access
- ID generation: Simple counter variable

**Trade-offs**:
- ✅ Simplicity - no external dependencies or setup
- ✅ Fast access - in-memory operations
- ❌ No persistence - data lost on exit (acceptable per Phase I scope)

## Testing Framework

### Decision: unittest (Python Standard Library)
**Rationale**: Part of Python standard library, no external dependencies required
**Alternatives considered**:
- pytest: Rejected (requires external dependency, violates constitution)
- nose2: Rejected (requires external dependency, violates constitution)

**unittest capabilities**:
- Test discovery
- Assertions
- Test fixtures (setup/teardown)
- Mocking (unittest.mock)

## Architecture Pattern

### Decision: Three-Layer Architecture (Models, Services, CLI)
**Rationale**: Constitution requires "clear separation of concerns" with models, services, and CLI separated into distinct modules
**Layer responsibilities**:

1. **Models Layer** (`src/models/task.py`):
   - Task class definition
   - Task entity attributes (id, title, description, completed)
   - No business logic (pure data structure)

2. **Services Layer** (`src/services/todo_service.py`):
   - Business logic for CRUD operations
   - Task storage management (list + dict)
   - ID generation
   - Validation logic (empty title check)
   - Error handling

3. **CLI Layer** (`src/cli/menu.py`):
   - User interface (menu display)
   - Input collection and validation
   - Output formatting
   - Application loop

**Alternatives considered**:
- Single-file script: Rejected (violates separation of concerns)
- MVC pattern: Rejected (over-engineering for CLI app)
- Repository pattern: Rejected (unnecessary abstraction for in-memory storage)

## Input Validation Strategy

### Decision: Early Validation at CLI Layer
**Rationale**: Fail fast - catch invalid input before calling services
**Validation points**:
1. **CLI Layer**: Menu option validation, ID format validation (numeric), empty input detection
2. **Service Layer**: Title non-empty validation, ID existence checks

**Error handling approach**:
- Use descriptive error messages
- Never crash on invalid input (constitutional requirement)
- Return to menu after errors
- Use try-except for input parsing (e.g., converting string to int)

## ID Generation Strategy

### Decision: Simple Counter with No Reuse
**Rationale**: Specification assumption states "Task IDs will continue to increment even after deletions (no ID reuse)"
**Implementation**:
```python
class TodoService:
    def __init__(self):
        self._next_id = 1
        self._tasks = []
        self._task_dict = {}

    def add_task(self, title, description):
        task = Task(self._next_id, title, description, False)
        self._next_id += 1  # Always increment, never reuse
        ...
```

**Alternatives considered**:
- UUID: Rejected (overkill for single-user in-memory app, not auto-incremented integers)
- Reuse deleted IDs: Rejected (violates specification assumption)

## User Interface Design

### Decision: Numbered Menu with Input Prompts
**Rationale**: Constitution mandates "menu-driven interaction using numbered options"
**Menu structure**:
```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice (1-6): _
```

**Interaction flow**:
1. Display menu
2. Accept numeric input
3. Validate choice (1-6)
4. Execute operation
5. Display result/confirmation
6. Return to menu (unless Exit selected)

**Error handling**:
- Invalid numbers (0, 7, 99): Display error, re-show menu
- Non-numeric input: Display error, re-show menu
- No crash on any input

## Display Format for Tasks

### Decision: Tabular Text Format
**Rationale**: Specification requires "ID, Title, Completion status (Completed/Pending)" to be shown
**Format example**:
```
ID | Title              | Status
----------------------------------------
1  | Buy groceries      | Pending
2  | Fix bug            | Completed
3  | Write report       | Pending
```

**Alternatives considered**:
- JSON output: Rejected (not user-friendly for CLI)
- Verbose list: Rejected (less scannable)

## Edge Cases and Decisions

### Empty Task List
**Decision**: Display friendly message "No tasks found. Add a task to get started!"
**Rationale**: Better UX than showing empty table

### Whitespace-Only Title
**Decision**: Treat as invalid (same as empty title)
**Implementation**: Strip whitespace, then check if empty
**Rationale**: Specification assumption states "Whitespace-only titles are considered invalid"

### Very Long Titles/Descriptions
**Decision**: No length limit (system memory is the limit)
**Rationale**: Specification assumption states "Task titles and descriptions have no maximum length constraints"
**Handling**: Display will truncate for readability if needed, but store full content

### Non-Existent Task ID
**Decision**: Display clear error message "Task with ID {id} not found"
**Rationale**: Required by FR-008 in specification

### Invalid Menu Input
**Decision**: Display "Invalid choice. Please enter a number between 1 and 6."
**Rationale**: Constitutional requirement for graceful error handling

## Performance Considerations

### Search Efficiency
**Decision**: Dual storage (list + dictionary)
**Rationale**: Balance between ordered display and fast lookup
- List: O(n) iteration for display (acceptable for <1000 tasks)
- Dict: O(1) lookup by ID for updates/deletes

### Memory Management
**Decision**: No special memory management
**Rationale**: Python's garbage collection handles cleanup automatically
**Expected usage**: ~1KB per task × 1000 tasks = ~1MB total (negligible)

## Exit Behavior

### Decision: Immediate Exit with Goodbye Message
**Rationale**: Specification states "application exits immediately (no persistence required per Phase I constraints)"
**Implementation**: Display "Goodbye!" message and terminate cleanly
**No save prompt**: Data loss on exit is expected and acceptable per Phase I scope

## Testing Strategy

### Decision: Unit Tests for Each Layer
**Test coverage**:
1. **Model tests**: Task object creation, attribute validation
2. **Service tests**: CRUD operations, ID generation, error cases
3. **CLI tests**: Input validation, menu display (if feasible)

**Test framework**: unittest from Python standard library
**Test location**: `tests/unit/` directory per template structure

**Note**: Integration and contract tests are optional per tasks template guidance and not required for Phase I

## Summary of Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| Language | Python 3.13+ | Constitutional requirement |
| Dependencies | Standard library only | Constitutional requirement (Principle IV) |
| Storage | In-memory (list + dict) | Constitutional prohibition of persistence |
| Architecture | 3-layer (Models/Services/CLI) | Constitutional requirement for separation of concerns |
| Testing | unittest | Standard library, no external deps |
| ID Generation | Auto-increment counter (no reuse) | Specification assumption |
| UI Pattern | Numbered menu | Constitutional requirement |
| Error Handling | Graceful with messages | Constitutional requirement |

## Open Questions

None. All technical decisions are fully specified and resolved.

## References

1. Project Constitution: `.specify/memory/constitution.md`
2. Feature Specification: `specs/001-todo-app/spec.md`
3. Python Documentation: https://docs.python.org/3/
4. unittest Documentation: https://docs.python.org/3/library/unittest.html
