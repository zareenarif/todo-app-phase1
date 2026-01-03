# Phase I Todo Application

A simple, in-memory command-line todo application built with Python 3.13+ following Spec-Driven Development (SDD) principles.

## Overview

This is a menu-driven CLI application for managing todo tasks during a single session. All data is stored in memory and is cleared when the application exits (no persistence).

**Features:**
- ✅ Add tasks with title and optional description
- ✅ View all tasks with ID, title, and completion status
- ✅ Search tasks by keyword (title or description)
- ✅ Filter tasks by completion status (All/Pending/Completed)
- ✅ Sort tasks by ID, title, or status
- ✅ Update existing task details
- ✅ Delete tasks
- ✅ Toggle task completion status (Pending ↔ Completed)
- ✅ Graceful error handling
- ✅ Clean, menu-driven interface

## Requirements

- **Python**: 3.13 or higher
- **Dependencies**: None (Python standard library only)
- **Operating System**: Windows, Linux, or macOS

## Quick Start

### 1. Verify Python Version

```bash
python --version
# or
python3 --version
# Expected: Python 3.13.x or higher
```

### 2. Run the Application

```bash
python main.py
# or
python3 main.py
```

### 3. Use the Application

You'll see a numbered menu:

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

**Example Workflow:**

1. Select `1` to add a task
   - Enter title: "Buy groceries"
   - Enter description (or press Enter to skip)

2. Select `2` to view all tasks
   - See your task list with IDs and statuses

3. Select `6` to search/filter tasks
   - Enter keyword: "buy" (or press Enter to skip)
   - Choose filter: Pending only, Completed only, or All
   - See matching tasks

4. Select `7` to sort tasks
   - Choose sort: by ID, Title, or Status
   - See tasks in sorted order

5. Select `5` to mark a task complete
   - Enter task ID
   - Status toggles between Pending and Completed

6. Select `8` to exit
   - All data is cleared (no persistence)

## Project Structure

```
todo-app-phase1/
├── src/
│   ├── models/
│   │   └── task.py              # Task entity (id, title, description, completed)
│   ├── services/
│   │   └── todo_service.py      # Business logic (CRUD operations)
│   └── cli/
│       └── menu.py               # CLI interface and menu loop
├── main.py                       # Application entry point
├── specs/                        # SDD documentation
│   └── 001-todo-app/
│       ├── spec.md               # Feature specification
│       ├── plan.md               # Implementation plan
│       ├── data-model.md         # Data model documentation
│       ├── quickstart.md         # Developer quickstart guide
│       ├── tasks.md              # Implementation tasks
│       └── contracts/
│           └── cli-interface.md  # CLI interface specification
├── .specify/
│   └── memory/
│       └── constitution.md       # Project constitution (SDD principles)
└── README.md                     # This file
```

## Design Principles

This project follows **Spec-Driven Development (SDD)** as defined in `.specify/memory/constitution.md`:

1. **Specification Before Implementation**: Complete spec created before coding
2. **Planning Before Coding**: Architectural plan approved before implementation
3. **Tasks Before Execution**: Work broken into discrete, testable tasks
4. **Simplicity Over Complexity**: Python standard library only, minimal architecture
5. **No Features Beyond Phase I Scope**: Strictly scoped to approved requirements

## Technical Details

**Architecture**: Three-layer separation of concerns
- **Models** (`src/models/`): Task entity with validation
- **Services** (`src/services/`): Business logic and in-memory storage
- **CLI** (`src/cli/`): User interface and menu loop

**Storage**: Dual structure for efficiency
- **List**: Maintains task order for display
- **Dictionary**: Provides O(1) lookup by task ID

**Data Model**:
- **Task ID**: Auto-incremented integer (no reuse after deletion)
- **Title**: Required, non-empty string
- **Description**: Optional string
- **Completed**: Boolean (default: False)

## Validation

All operations include input validation:
- ✅ Empty titles rejected
- ✅ Invalid menu options handled gracefully
- ✅ Non-existent task IDs return clear error messages
- ✅ Application never crashes on invalid input

## Limitations (By Design)

This is Phase I - intentionally simple and focused:

- ❌ **No Persistence**: Data lost on exit (in-memory only)
- ❌ **No Database**: Uses Python lists and dictionaries
- ❌ **No GUI**: Command-line interface only
- ❌ **No External Dependencies**: Standard library only
- ❌ **Single User**: No multi-user support
- ❌ **No Search/Filter**: View shows all tasks
- ❌ **No Due Dates**: Tasks have no time-based features
- ❌ **No Categories/Tags**: Simple flat task list

## Development

### Code Quality

All code adheres to constitutional quality standards:
- ✅ Clean, readable code with clear variable names
- ✅ Small, focused functions with single responsibilities
- ✅ Comprehensive docstrings for all classes and methods
- ✅ No dead code or unused imports

### Testing

Manual testing against acceptance scenarios from `specs/001-todo-app/spec.md`:
- 6 user stories with 18 acceptance scenarios
- All scenarios validated manually
- Independent test criteria for each user story

### Future Phases

Phase I is intentionally minimal. Future phases may include:
- Persistent storage (database or file system)
- Task prioritization and categorization
- Due dates and reminders
- Search and filtering
- Web or GUI interface
- Multi-user support

## Documentation

Comprehensive SDD documentation available in `specs/001-todo-app/`:

- **spec.md**: Complete feature specification with user stories and requirements
- **plan.md**: Implementation plan with architecture decisions
- **data-model.md**: Detailed entity structure and validation rules
- **tasks.md**: Complete task breakdown (31 tasks)
- **quickstart.md**: Developer quickstart guide
- **contracts/cli-interface.md**: Complete CLI specification

## License

This is a demonstration project for Spec-Driven Development.

## Acknowledgments

Built with Claude Code following constitutional SDD principles.

---

**Phase I Todo Application** - Simple. Reliable. In-Memory.
