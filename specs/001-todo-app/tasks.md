---

description: "Task list for Phase I Todo Application implementation"
---

# Tasks: Phase I Todo Application

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL and not included per Phase I specification (no TDD requirement mentioned)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure (src/models, src/services, src/cli, tests/unit)
- [x] T002 [P] Create empty __init__.py files in src/, src/models/, src/services/, src/cli/ for Python package structure
- [x] T003 [P] Create main.py application entry point in project root

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Task model class in src/models/task.py with attributes (id, title, description, completed) and validation for non-empty title
- [x] T005 Create TodoService class in src/services/todo_service.py with initialization (__init__ method setting up empty task list, task dict, and next_id counter)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add tasks with title (required) and optional description

**Independent Test**: Launch app, select "Add Task", provide title and optional description, verify task created with unique ID and "Pending" status

### Implementation for User Story 1

- [x] T006 [US1] Implement add_task method in src/services/todo_service.py (validate title non-empty, create Task, assign ID, increment counter, store in list and dict, return task)
- [x] T007 [US1] Implement display_menu function in src/cli/menu.py (print menu with 6 numbered options: Add Task, View Tasks, Update Task, Delete Task, Mark Complete/Incomplete, Exit)
- [x] T008 [US1] Implement get_menu_choice function in src/cli/menu.py (get user input, validate 1-6, handle invalid input gracefully, return choice)
- [x] T009 [US1] Implement handle_add_task function in src/cli/menu.py (prompt for title, validate non-empty, prompt for optional description, call service.add_task, display success message with task details)
- [x] T010 [US1] Implement main application loop in src/cli/menu.py (run_menu function: initialize service, loop displaying menu, get choice, call appropriate handler, continue until Exit)
- [x] T011 [US1] Wire up main.py to call run_menu from src/cli/menu.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Display all tasks with ID, title, and completion status

**Independent Test**: Add several tasks with different completion statuses, select "View Tasks", verify all tasks displayed with correct information

### Implementation for User Story 2

- [x] T012 [US2] Implement get_all_tasks method in src/services/todo_service.py (return list of all tasks)
- [x] T013 [US2] Implement handle_view_tasks function in src/cli/menu.py (call service.get_all_tasks, format and display as table with ID/Title/Status columns, handle empty list with friendly message)
- [x] T014 [US2] Integrate handle_view_tasks into main loop in src/cli/menu.py (add to menu choice handler for option 2)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 5 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Toggle completion status of tasks to track progress

**Independent Test**: Create task, select "Mark Task Complete/Incomplete", provide task ID, verify status toggles between Completed and Pending

### Implementation for User Story 5

- [x] T015 [US5] Implement get_task_by_id method in src/services/todo_service.py (lookup task in dict, return task or None)
- [x] T016 [US5] Implement toggle_task_completion method in src/services/todo_service.py (get task by ID, toggle completed boolean, return success or error if not found)
- [x] T017 [US5] Implement handle_toggle_completion function in src/cli/menu.py (prompt for task ID, validate numeric input, call service.toggle_task_completion, display success with new status or error message)
- [x] T018 [US5] Integrate handle_toggle_completion into main loop in src/cli/menu.py (add to menu choice handler for option 5)

**Checkpoint**: At this point, User Stories 1, 2, AND 5 should all work independently

---

## Phase 6: User Story 3 - Update Existing Task (Priority: P2)

**Goal**: Allow users to modify task title and/or description

**Independent Test**: Create task, select "Update Task", provide task ID and new title/description, verify changes saved

### Implementation for User Story 3

- [x] T019 [US3] Implement update_task method in src/services/todo_service.py (get task by ID, validate new title if provided, update title and/or description, return success or error if not found)
- [x] T020 [US3] Implement handle_update_task function in src/cli/menu.py (prompt for task ID, display current values, prompt for new title/description with option to keep current, call service.update_task, display success or error)
- [x] T021 [US3] Integrate handle_update_task into main loop in src/cli/menu.py (add to menu choice handler for option 3)

**Checkpoint**: All P1 and P2 priority user stories should now be independently functional

---

## Phase 7: User Story 4 - Delete Task (Priority: P3)

**Goal**: Remove tasks that are no longer relevant

**Independent Test**: Create task, select "Delete Task", provide task ID, verify task removed from list

### Implementation for User Story 4

- [x] T022 [US4] Implement delete_task method in src/services/todo_service.py (get task by ID, remove from list and dict, return success or error if not found)
- [x] T023 [US4] Implement handle_delete_task function in src/cli/menu.py (prompt for task ID, display task title, prompt for confirmation y/n, call service.delete_task if confirmed, display success or cancellation message)
- [x] T024 [US4] Integrate handle_delete_task into main loop in src/cli/menu.py (add to menu choice handler for option 4)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: User Story 6 - Exit Application (Priority: P1)

**Goal**: Provide clean application termination

**Independent Test**: Select "Exit" from menu, verify goodbye message displayed and application terminates

### Implementation for User Story 6

- [x] T025 [US6] Implement handle_exit function in src/cli/menu.py (display goodbye message, return signal to exit loop)
- [x] T026 [US6] Integrate handle_exit into main loop in src/cli/menu.py (add to menu choice handler for option 6, break loop on exit signal)

**Checkpoint**: All user stories complete - application is fully functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T027 [P] Add input validation helper function in src/cli/menu.py (validate_integer_input for task IDs)
- [x] T028 [P] Add error message constants in src/cli/menu.py (standard error messages for consistency)
- [x] T029 [P] Review and refactor code for simplicity and readability per constitutional quality standards
- [x] T030 [P] Add docstrings to all classes and public methods (Task, TodoService, menu functions)
- [x] T031 Create README.md in project root with project overview, setup instructions, and usage examples

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (P1): Add Task - No dependencies on other stories
  - User Story 2 (P1): View Tasks - No dependencies on other stories (works independently)
  - User Story 5 (P2): Mark Complete - Depends on US1 for testing but independently implementable
  - User Story 3 (P2): Update Task - Depends on US1 for testing but independently implementable
  - User Story 4 (P3): Delete Task - Depends on US1 for testing but independently implementable
  - User Story 6 (P1): Exit - No dependencies (can be implemented anytime after US1)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

**All user stories are independently implementable after Foundational phase**. Dependencies shown are for testing convenience only:

- **User Story 1 (Add Task)**: Foundation only (Task model + TodoService initialized)
- **User Story 2 (View Tasks)**: Foundation only (can display empty list)
- **User Story 5 (Mark Complete)**: Foundation only (can return "not found" error initially)
- **User Story 3 (Update Task)**: Foundation only (can return "not found" error initially)
- **User Story 4 (Delete Task)**: Foundation only (can return "not found" error initially)
- **User Story 6 (Exit)**: Foundation only (can exit from empty menu)

**For meaningful end-to-end testing**, implement in priority order: US1 → US2 → US5 → US3 → US4 → US6

### Within Each User Story

Each user story follows this internal order:
1. Service layer methods (business logic)
2. CLI handler functions (user interface)
3. Integration into main menu loop

Tasks within a user story are sequential and must be completed in order.

### Parallel Opportunities

- **Setup phase**: All tasks can run in parallel (T001, T002, T003)
- **Foundational phase**: T004 and T005 can run in parallel (Task model and TodoService are independent)
- **Polish phase**: T027, T028, T029, T030, T031 can all run in parallel

**User stories CANNOT run in parallel** because they share the same files (menu.py, todo_service.py). However, with multiple developers:
- One developer could implement service methods while another implements CLI handlers (if carefully coordinated)
- Different user stories must be implemented sequentially to avoid merge conflicts

---

## Parallel Example: Setup Phase

```bash
# Launch all setup tasks together:
Task: "Create project directory structure"
Task: "Create empty __init__.py files"
Task: "Create main.py application entry point"
# All three can execute simultaneously
```

## Parallel Example: Foundational Phase

```bash
# Launch foundational tasks together:
Task: "Create Task model class in src/models/task.py"
Task: "Create TodoService class in src/services/todo_service.py"
# Both can execute simultaneously (different files)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T005)
3. Complete Phase 3: User Story 1 - Add Task (T006-T011)
4. **STOP and VALIDATE**: Test adding tasks manually
5. Deploy/demo if ready

**MVP Delivers**: Ability to add tasks and see them in memory. App has a menu but most options don't work yet.

### MVP+ (User Stories 1 & 2)

Continue from MVP:
4. Complete Phase 4: User Story 2 - View Tasks (T012-T014)
5. **VALIDATE**: Test add + view workflow
6. Deploy/demo

**MVP+ Delivers**: Core task creation and visibility. Users can add tasks and see their list.

### Incremental Delivery (Priority Order)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Add) → Test independently → Deploy/Demo (MVP! 🎯)
3. Add User Story 2 (View) → Test independently → Deploy/Demo (MVP+)
4. Add User Story 5 (Toggle) → Test independently → Deploy/Demo
5. Add User Story 3 (Update) → Test independently → Deploy/Demo
6. Add User Story 4 (Delete) → Test independently → Deploy/Demo
7. Add User Story 6 (Exit) → Test independently → Deploy/Demo
8. Add Polish tasks → Final release

Each user story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers (not recommended for this small project, but for illustration):

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: Implements User Story 1 (US1)
   - Wait for A to finish (US1 establishes menu.py and todo_service.py structure)
3. After US1 complete:
   - Developer B: User Story 2 (adds to existing files)
   - Developer C: User Story 5 (adds to existing files)
   - **Must coordinate** to avoid conflicts in menu.py

**Recommended for Phase I**: Single developer, sequential implementation in priority order.

---

## Task Statistics

**Total Tasks**: 31
- Setup: 3 tasks (T001-T003)
- Foundational: 2 tasks (T004-T005)
- User Story 1 (P1): 6 tasks (T006-T011) 🎯 MVP
- User Story 2 (P1): 3 tasks (T012-T014)
- User Story 5 (P2): 4 tasks (T015-T018)
- User Story 3 (P2): 3 tasks (T019-T021)
- User Story 4 (P3): 3 tasks (T022-T024)
- User Story 6 (P1): 2 tasks (T025-T026)
- Polish: 5 tasks (T027-T031)

**Parallel Opportunities**: 8 tasks can run in parallel (marked with [P])
**Sequential Tasks**: 23 tasks must run in sequence

**Estimated Effort**:
- Setup: ~30 minutes
- Foundational: ~1 hour
- User Story 1 (MVP): ~2-3 hours
- User Story 2: ~1 hour
- User Story 5: ~1.5 hours
- User Story 3: ~1 hour
- User Story 4: ~1 hour
- User Story 6: ~30 minutes
- Polish: ~1-2 hours

**Total Estimated Time**: ~8-10 hours for complete implementation

---

## Notes

- Tasks follow constitutional principle: specification → planning → tasks → execution
- Each task is specific with exact file paths for immediate executability
- User stories are independently testable after their phase completes
- No tests included per Phase I specification (tests are optional and not requested)
- Verify against acceptance scenarios from spec.md after completing each user story
- Stop at any checkpoint to validate story independently
- Follow constitutional quality standards: clean code, small functions, no dead code
- All code must be generated by Claude Code (no manual coding)

---

## Validation Checklist

After completing all tasks, verify:

**Functional Requirements (from spec.md)**:
- [ ] FR-001 through FR-015 all satisfied

**Success Criteria (from spec.md)**:
- [ ] SC-001 through SC-007 all met

**Constitutional Compliance**:
- [ ] Python 3.13+ used
- [ ] Standard library only (no external deps)
- [ ] In-memory storage (no persistence)
- [ ] CLI interface only
- [ ] Separation of concerns (models/services/CLI)
- [ ] Clean, readable code
- [ ] No dead code

**User Story Acceptance Scenarios**:
- [ ] User Story 1: All 3 acceptance scenarios pass
- [ ] User Story 2: All 3 acceptance scenarios pass
- [ ] User Story 3: All 3 acceptance scenarios pass
- [ ] User Story 4: All 3 acceptance scenarios pass
- [ ] User Story 5: All 3 acceptance scenarios pass
- [ ] User Story 6: All 2 acceptance scenarios pass

**Edge Cases (from spec.md)**:
- [ ] Invalid menu options handled gracefully
- [ ] Very long titles/descriptions accepted
- [ ] Whitespace-only titles rejected
- [ ] ID increments continue after deletions
- [ ] Empty task list displays friendly message
