# Quickstart Guide: Phase I Todo Application

**Feature**: 001-todo-app
**Date**: 2026-01-03
**Status**: Complete

## Overview

This quickstart guide provides step-by-step instructions for developers to understand, build, run, and validate the Phase I Todo Application.

## Prerequisites

### Required
- **Python**: Version 3.13 or higher
- **Operating System**: Windows, Linux, or macOS (cross-platform)
- **Terminal/Command Line**: Any terminal with Python access

### Verification Commands

```bash
# Check Python version (must be 3.13+)
python --version
# or
python3 --version

# Expected output: Python 3.13.x or higher
```

### No External Dependencies
This project uses **only** the Python standard library. No `pip install` or virtual environment setup required (though virtual environments are recommended for cleanliness).

## Project Structure

```
todo-app-phase1/
├── src/
│   ├── models/
│   │   └── task.py           # Task entity class
│   ├── services/
│   │   └── todo_service.py   # Business logic (CRUD operations)
│   └── cli/
│       └── menu.py            # CLI interface and main loop
├── tests/
│   └── unit/
│       ├── test_task.py       # Task model tests
│       ├── test_todo_service.py  # Service layer tests
│       └── test_cli.py        # CLI tests (optional)
├── main.py                    # Application entry point
├── specs/
│   └── 001-todo-app/
│       ├── spec.md            # Feature specification
│       ├── plan.md            # Implementation plan
│       ├── data-model.md      # Data model documentation
│       ├── quickstart.md      # This file
│       └── contracts/
│           └── cli-interface.md  # CLI contract
└── .specify/
    └── memory/
        └── constitution.md    # Project constitution
```

## Quick Start (5 Minutes)

### Step 1: Navigate to Project Directory

```bash
cd /path/to/todo-app-phase1
```

### Step 2: Run the Application

```bash
python main.py
# or
python3 main.py
```

**Expected Output**:
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

### Step 3: Try Basic Operations

#### Add a Task
```
Enter your choice (1-6): 1

=== Add Task ===

Enter task title: Buy groceries
Enter task description (optional, press Enter to skip):

✓ Task added successfully!
  ID: 1
  Title: Buy groceries
  Description: None
  Status: Pending
```

#### View Tasks
```
Enter your choice (1-6): 2

=== All Tasks ===

ID | Title              | Status
-----------------------------------------
1  | Buy groceries      | Pending

Total: 1 task
```

#### Exit Application
```
Enter your choice (1-6): 6

Goodbye! All tasks have been cleared.
```

## Development Workflow

### Step 1: Review the Specification

Read the following documents in order:
1. **Constitution** (`.specify/memory/constitution.md`): Understand project principles
2. **Specification** (`specs/001-todo-app/spec.md`): Understand user requirements
3. **Implementation Plan** (`specs/001-todo-app/plan.md`): Understand technical approach
4. **Data Model** (`specs/001-todo-app/data-model.md`): Understand entity structure
5. **CLI Contract** (`specs/001-todo-app/contracts/cli-interface.md`): Understand interface

### Step 2: Create Directory Structure

```bash
# From project root
mkdir -p src/models src/services src/cli tests/unit
```

### Step 3: Implement Components (TDD Approach)

Following the constitution's "Tasks Before Execution" principle, you would:

1. Run `/sp.tasks` to generate task list
2. Implement tasks in order (models → services → CLI)
3. Write tests first (if TDD specified)
4. Implement functionality to pass tests
5. Verify against acceptance criteria

**Implementation Order** (from tasks.md):
1. Task model (`src/models/task.py`)
2. TodoService (`src/services/todo_service.py`)
3. CLI Menu (`src/cli/menu.py`)
4. Main entry point (`main.py`)
5. Unit tests (`tests/unit/`)

### Step 4: Run Tests

```bash
# Run all tests
python -m unittest discover -s tests/unit -p "test_*.py"

# Run specific test file
python -m unittest tests/unit/test_task.py

# Run with verbose output
python -m unittest discover -s tests/unit -v
```

**Expected Output** (all tests passing):
```
.......
----------------------------------------------------------------------
Ran 7 tests in 0.002s

OK
```

### Step 5: Manual Testing

Follow the test scenarios from `specs/001-todo-app/spec.md`:

#### Test Scenario 1: Add Task with Title Only
1. Launch app: `python main.py`
2. Select option 1 (Add Task)
3. Enter title: "Buy groceries"
4. Press Enter to skip description
5. **Verify**: Task created with ID 1, status Pending

#### Test Scenario 2: Add Task with Title and Description
1. Select option 1
2. Enter title: "Fix bug"
3. Enter description: "Update validation logic"
4. **Verify**: Task created with ID 2

#### Test Scenario 3: View All Tasks
1. Select option 2 (View Tasks)
2. **Verify**: Both tasks displayed with correct IDs, titles, and statuses

#### Test Scenario 4: Mark Task Complete
1. Select option 5
2. Enter ID: 1
3. **Verify**: Task 1 status changes to Completed

#### Test Scenario 5: Update Task
1. Select option 3
2. Enter ID: 1
3. Update title to: "Buy milk and groceries"
4. **Verify**: Title updated, status remains Completed

#### Test Scenario 6: Delete Task
1. Select option 4
2. Enter ID: 2
3. Confirm deletion: y
4. **Verify**: Task 2 removed from list

#### Test Scenario 7: Exit Application
1. Select option 6
2. **Verify**: Goodbye message displayed, app exits

## Common Use Cases

### Use Case 1: Daily Task Management

```bash
# Start of day: Add tasks
python main.py
> 1 (Add Task)
> "Review pull requests"
> "Morning standup"
> (etc.)

# During day: Mark tasks complete
> 5 (Mark Complete)
> 1
> 2
> (etc.)

# View progress
> 2 (View Tasks)

# End of day: Exit (all data cleared)
> 6 (Exit)
```

### Use Case 2: Quick Todo Capture

```bash
python main.py
> 1
> "Call dentist"
> (skip description)

> 1
> "Buy birthday gift"
> (skip description)

> 2  # View all
> 6  # Exit
```

### Use Case 3: Task Refinement

```bash
python main.py
> 1
> "Task placeholder"
> (skip description)

> 3  # Update task
> 1
> "Finalized task name"
> "Detailed description of what needs to be done"

> 2  # Verify update
> 6  # Exit
```

## Validation Checklist

Use this checklist to verify the implementation meets all requirements:

### Functional Requirements (FR)

- [ ] **FR-001**: Add task with required title and optional description
- [ ] **FR-002**: Task ID auto-generated and unique
- [ ] **FR-003**: New tasks default to completed=False
- [ ] **FR-004**: View displays ID, title, and status
- [ ] **FR-005**: Update task title and/or description by ID
- [ ] **FR-006**: Delete task by ID
- [ ] **FR-007**: Toggle completion status by ID
- [ ] **FR-008**: Error message for non-existent task IDs
- [ ] **FR-009**: Error message for empty task title
- [ ] **FR-010**: Menu shows 6 numbered options
- [ ] **FR-011**: Continuous loop until Exit selected
- [ ] **FR-012**: Graceful handling of invalid input
- [ ] **FR-013**: In-memory storage only (no persistence)
- [ ] **FR-014**: Confirmation messages after operations
- [ ] **FR-015**: Clean termination on Exit

### Success Criteria (SC)

- [ ] **SC-001**: Add task completes in < 1 second
- [ ] **SC-002**: View tasks completes in < 1 second
- [ ] **SC-003**: Complete workflow (add → view → mark → view) works without errors
- [ ] **SC-004**: Invalid inputs show clear errors without crashes
- [ ] **SC-005**: Stable memory usage with 1000 tasks
- [ ] **SC-006**: All operations work without external documentation
- [ ] **SC-007**: Startup time < 2 seconds

### Constitutional Compliance

- [ ] Python 3.13+ used
- [ ] No external dependencies (standard library only)
- [ ] In-memory storage (no database/files)
- [ ] CLI interface only (no GUI/web)
- [ ] Separation of concerns (models/services/CLI separate)
- [ ] Clean, readable code
- [ ] No dead code

### Edge Cases

- [ ] Empty title rejected
- [ ] Whitespace-only title rejected
- [ ] Invalid menu options handled gracefully
- [ ] Non-existent task IDs handled gracefully
- [ ] Very long titles/descriptions accepted
- [ ] Empty task list displays friendly message
- [ ] ID increments continue after deletions (no reuse)

## Troubleshooting

### Issue: Python version too old

**Symptom**: Application fails to run or syntax errors
**Solution**:
```bash
# Check version
python --version

# If < 3.13, upgrade Python or use python3.13 explicitly
python3.13 main.py
```

### Issue: Module not found errors

**Symptom**: `ModuleNotFoundError: No module named 'src'`
**Solution**:
```bash
# Ensure you're in project root directory
pwd  # Should show .../todo-app-phase1

# Try with Python path
PYTHONPATH=. python main.py

# Or run as module
python -m src.cli.menu
```

### Issue: Tests fail with import errors

**Symptom**: Tests can't import `src.models.task`
**Solution**:
```bash
# Run from project root
cd /path/to/todo-app-phase1

# Ensure PYTHONPATH includes current directory
PYTHONPATH=. python -m unittest discover -s tests/unit
```

### Issue: Application doesn't display symbols correctly

**Symptom**: ✓ and ✗ display as `?` or boxes
**Solution**: This is a terminal encoding issue. The app still works; only display is affected. Alternative: use `[OK]` and `[ERROR]` instead of symbols.

## Performance Testing

### Test with 1000 Tasks

```python
# Create test script: test_performance.py
from src.services.todo_service import TodoService
import time

service = TodoService()

# Add 1000 tasks
start = time.time()
for i in range(1000):
    service.add_task(f"Task {i}", f"Description {i}")
duration = time.time() - start
print(f"Added 1000 tasks in {duration:.2f} seconds")

# View all tasks
start = time.time()
tasks = service.get_all_tasks()
duration = time.time() - start
print(f"Retrieved {len(tasks)} tasks in {duration:.2f} seconds")

# Expected: Both operations < 1 second
```

## Next Steps

After validating the implementation:

1. **Code Review**: Review code against constitution quality standards
2. **Documentation**: Ensure inline comments explain complex logic
3. **Refactoring**: Simplify any over-engineered code
4. **User Testing**: Have someone unfamiliar with the code try the app
5. **Phase II Planning**: If approved, begin planning persistence features

## Additional Resources

- **Python Documentation**: https://docs.python.org/3/
- **unittest Documentation**: https://docs.python.org/3/library/unittest.html
- **PEP 8 Style Guide**: https://peps.python.org/pep-0008/

## Support

For issues or questions:
1. Review the specification: `specs/001-todo-app/spec.md`
2. Check the constitution: `.specify/memory/constitution.md`
3. Verify against CLI contract: `specs/001-todo-app/contracts/cli-interface.md`

## Changelog

- **2026-01-03**: Initial quickstart guide created
