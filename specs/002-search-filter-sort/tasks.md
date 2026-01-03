---

description: "Task list for Feature 002: Search, Filter, and Sort capabilities"
---

# Tasks: Search, Filter, and Sort Capabilities

**Input**: Design documents from `/specs/002-search-filter-sort/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/cli-interface.md, quickstart.md

**Tests**: Tests are OPTIONAL and not included per feature specification (manual testing recommended)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow single project structure from plan.md

---

## Phase 1: Verification (Prerequisites)

**Purpose**: Verify Phase I application is complete and ready for enhancement

- [x] T001 Verify Phase I application runs successfully with `python main.py`
- [x] T002 Verify all existing features work (Add, View, Update, Delete, Toggle, Exit)
- [x] T003 Verify constitution v1.1.0 amendment is in place (allows controlled enhancement)

---

## Phase 2: Foundational (Shared Infrastructure)

**Purpose**: Menu framework updates that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Update display_menu() function in src/cli/menu.py to show 8 options (add placeholders for options 6-7, move Exit to 8)
- [x] T005 Update get_menu_choice() function in src/cli/menu.py to validate 1-8 instead of 1-6
- [x] T006 Add placeholder handlers in run_menu() function in src/cli/menu.py for options 6-7 (can print "Coming soon")

**Checkpoint**: Menu framework ready - user story implementation can now begin in parallel or sequentially

---

## Phase 3: User Story 1 - Search Tasks by Keyword (Priority: P1) 🎯 MVP

**Goal**: Allow users to search for tasks by entering keywords that match against title or description

**Independent Test**: Add 10+ tasks with distinct titles, select "Search Tasks" from menu, enter a keyword, verify only matching tasks appear

### Implementation for User Story 1

- [x] T007 [US1] Implement search_tasks(keyword) method in src/services/todo_service.py (case-insensitive substring matching in title or description)
- [x] T008 [US1] Add get_filter_choice() helper function in src/cli/menu.py (for filter selection: All/Pending/Completed)
- [x] T009 [US1] Implement handle_search_filter_tasks(service) function in src/cli/menu.py (search only, default to "All tasks" filter)
- [x] T010 [US1] Wire handle_search_filter_tasks to option 6 in run_menu() function in src/cli/menu.py
- [x] T011 [US1] Update display_menu() to change option 6 from placeholder to "Search/Filter Tasks"

**Checkpoint**: At this point, User Story 1 (search only) should be fully functional and testable independently

---

## Phase 4: User Story 2 - Filter Tasks by Status (Priority: P1)

**Goal**: Allow users to filter tasks to show only completed or only pending tasks

**Independent Test**: Create mix of completed and pending tasks, select "Search/Filter Tasks" from menu, skip search (press Enter), choose "Pending only" filter, verify only incomplete tasks appear

### Implementation for User Story 2

- [x] T012 [US2] Implement filter_tasks(status_filter) method in src/services/todo_service.py (filter by 'all', 'pending', or 'completed')
- [x] T013 [US2] Enhance handle_search_filter_tasks() in src/cli/menu.py to call get_filter_choice() and apply filter
- [x] T014 [US2] Update handle_search_filter_tasks() result display logic to show appropriate header based on filter selection

**Checkpoint**: At this point, User Stories 1 AND 2 should both work (search, filter, or both together)

---

## Phase 5: User Story 4 - Combine Search and Filter (Priority: P2)

**Goal**: Apply both search keywords and status filters together to find specific tasks within a particular completion state

**Independent Test**: Create diverse task set, apply search keyword AND status filter, verify only tasks matching BOTH criteria appear

### Implementation for User Story 4

- [x] T015 [US4] Implement search_and_filter(keyword, status_filter) method in src/services/todo_service.py (combines search and filter operations)
- [x] T016 [US4] Update handle_search_filter_tasks() in src/cli/menu.py to use search_and_filter() instead of separate search/filter calls
- [x] T017 [US4] Enhance error messages in handle_search_filter_tasks() to handle combined no-results cases

**Checkpoint**: At this point, User Stories 1, 2, AND 4 work seamlessly (full search/filter integration)

---

## Phase 6: User Story 3 - Sort Tasks (Priority: P2)

**Goal**: Allow users to sort tasks by ID, title, or completion status in ascending or descending order

**Independent Test**: Create tasks in random order with varying titles and statuses, select "Sort Tasks" from menu, choose a sort criterion, verify tasks appear in correct order

### Implementation for User Story 3

- [x] T018 [P] [US3] Implement sort_tasks(sort_by, reverse) method in src/services/todo_service.py (sort by id/title/status with direction)
- [x] T019 [P] [US3] Implement get_sort_choice() helper function in src/cli/menu.py (for sort criterion selection: 6 options)
- [x] T020 [US3] Implement handle_sort_tasks(service) function in src/cli/menu.py (gets sort choice, displays sorted results)
- [x] T021 [US3] Wire handle_sort_tasks to option 7 in run_menu() function in src/cli/menu.py
- [x] T022 [US3] Update display_menu() to change option 7 from placeholder to "Sort Tasks"

**Checkpoint**: All primary user stories (1, 2, 3, 4) should now be independently functional

---

## Phase 7: User Story 5 - Clear Filters (Priority: P3)

**Goal**: Allow users to easily return to viewing all tasks in original order

**Independent Test**: Apply various search/filter/sort operations, select "View Tasks" (option 2), verify original task list appears in creation order

### Implementation for User Story 5

- [x] T023 [US5] Verify that handle_view_tasks() in src/cli/menu.py calls get_all_tasks() and returns original order
- [x] T024 [US5] Verify that returning to main menu clears any search/filter/sort state (operations are non-persistent)
- [x] T025 [US5] Add note to README.md explaining that search/filter/sort are temporary views (optional)

**Checkpoint**: All user stories complete - application has full search/filter/sort capabilities

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T026 [P] Add comprehensive docstrings to all 4 new service methods in src/services/todo_service.py
- [x] T027 [P] Add comprehensive docstrings to all 2 new validators in src/cli/menu.py
- [x] T028 [P] Add comprehensive docstrings to all 2 new handlers in src/cli/menu.py
- [x] T029 Review code for simplicity and readability per constitutional quality standards
- [x] T030 Update README.md with new features section documenting search/filter/sort capabilities
- [x] T031 Run full manual test suite from quickstart.md (all 5 test scenarios)
- [x] T032 Verify all edge cases from spec.md (empty search, invalid options, no matches, empty list)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Verification (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Verification completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User Story 1 (P1): Search - No dependencies on other stories
  - User Story 2 (P1): Filter - No dependencies on other stories (independent)
  - User Story 4 (P2): Combine - Logically depends on US1+US2 methods, but can be implemented together
  - User Story 3 (P2): Sort - No dependencies on other stories (completely independent)
  - User Story 5 (P3): Clear - Depends on viewing original list (existing functionality)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

**All user stories are independently implementable after Foundational phase**. Dependencies shown are for logical flow only:

- **User Story 1 (Search)**: Foundation only → Can implement and test search_tasks() independently
- **User Story 2 (Filter)**: Foundation only → Can implement and test filter_tasks() independently
- **User Story 4 (Combine)**: Uses US1+US2 methods → Implement search_and_filter() which calls search and filter logic
- **User Story 3 (Sort)**: Foundation only → Completely independent of search/filter functionality
- **User Story 5 (Clear)**: Uses existing get_all_tasks() → Just verify existing behavior works

**Recommended Implementation Order**: US1 → US2 → US4 → US3 → US5 (priority-driven with logical dependencies)

**Alternative Order**: US1 → US2 → US3 → US4 → US5 (strict priority order, works fine)

### Within Each User Story

Each user story follows this internal order:
1. Service layer methods (business logic)
2. CLI helper functions (validators)
3. CLI handler functions (user interface)
4. Integration into main menu loop

Tasks within a user story are sequential unless marked [P] for parallel execution.

### Parallel Opportunities

- **Verification phase**: T001, T002, T003 can run in parallel (independent checks)
- **Foundational phase**: T004, T005, T006 must run sequentially (same file, menu.py)
- **User Story 3**: T018 and T019 can run in parallel (different functions, service vs CLI)
- **Polish phase**: T026, T027, T028, T030 can run in parallel (different tasks, documentation)

**User stories CAN run in parallel** if multiple developers available:
- Developer A: US1 (Search)
- Developer B: US2 (Filter)
- Developer C: US3 (Sort)
- Then converge for US4 (Combine) which uses US1+US2

However, recommended for this small feature: **Sequential implementation in priority order** by single developer.

---

## Parallel Example: User Story 3 (Sort)

```bash
# Launch parallel tasks for User Story 3:
Task: "Implement sort_tasks(sort_by, reverse) method in src/services/todo_service.py"
Task: "Implement get_sort_choice() helper function in src/cli/menu.py"
# Both can execute simultaneously (different files, no dependencies)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Verification (T001-T003)
2. Complete Phase 2: Foundational (T004-T006)
3. Complete Phase 3: User Story 1 - Search (T007-T011)
4. **STOP and VALIDATE**: Test search functionality manually
5. Deploy/demo if ready

**MVP Delivers**: Ability to search tasks by keyword. Users can find specific tasks without scrolling through entire list.

### MVP+ (User Stories 1 & 2)

Continue from MVP:
4. Complete Phase 4: User Story 2 - Filter (T012-T014)
5. **VALIDATE**: Test search + filter workflow
6. Deploy/demo

**MVP+ Delivers**: Complete search and filter capabilities. Users can find tasks by keyword AND filter by completion status.

### Incremental Delivery (Priority Order)

1. Complete Verification + Foundational → Foundation ready
2. Add User Story 1 (Search) → Test independently → Deploy/Demo (MVP! 🎯)
3. Add User Story 2 (Filter) → Test independently → Deploy/Demo (MVP+)
4. Add User Story 4 (Combine) → Test independently → Deploy/Demo
5. Add User Story 3 (Sort) → Test independently → Deploy/Demo
6. Add User Story 5 (Clear) → Test independently → Deploy/Demo
7. Add Polish tasks → Final release

Each user story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers (not recommended for this small feature, but for illustration):

1. Team completes Verification + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Search)
   - Developer B: User Story 3 (Sort) - completely independent
3. After US1 complete:
   - Developer A: User Story 2 (Filter)
   - Developer B: Continues with US3
4. After US1 + US2 complete:
   - Developer A: User Story 4 (Combine)
   - Developer B: User Story 5 (Clear)

**Recommended for Feature 002**: Single developer, sequential implementation in priority order.

---

## Task Statistics

**Total Tasks**: 32
- Verification: 3 tasks (T001-T003)
- Foundational: 3 tasks (T004-T006)
- User Story 1 (P1): 5 tasks (T007-T011) 🎯 MVP
- User Story 2 (P1): 3 tasks (T012-T014)
- User Story 4 (P2): 3 tasks (T015-T017)
- User Story 3 (P2): 5 tasks (T018-T022)
- User Story 5 (P3): 3 tasks (T023-T025)
- Polish: 7 tasks (T026-T032)

**Parallel Opportunities**: 6 tasks can run in parallel (marked with [P])
**Sequential Tasks**: 26 tasks must run in sequence

**Estimated Effort**:
- Verification: ~15 minutes
- Foundational: ~30 minutes
- User Story 1 (MVP): ~1 hour
- User Story 2: ~45 minutes
- User Story 4: ~30 minutes
- User Story 3: ~1 hour
- User Story 5: ~15 minutes
- Polish: ~1 hour

**Total Estimated Time**: ~5-6 hours for complete implementation (matches quickstart estimate of 3-4 hours coding + 1-2 hours testing/polish)

---

## Notes

- Tasks follow constitutional principle: specification → planning → tasks → execution
- Each task is specific with exact file paths for immediate executability
- User stories are independently testable after their phase completes
- No tests included per feature specification (manual testing per quickstart.md)
- Verify against acceptance scenarios from spec.md after completing each user story
- Stop at any checkpoint to validate story independently
- Follow constitutional quality standards: clean code, small functions, comprehensive docstrings
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
- [ ] In-memory operations (no persistence)
- [ ] CLI interface only
- [ ] Separation of concerns (services/CLI)
- [ ] Clean, readable code
- [ ] Comprehensive docstrings
- [ ] No dead code

**User Story Acceptance Scenarios (from spec.md)**:
- [ ] User Story 1: All 4 acceptance scenarios pass
- [ ] User Story 2: All 4 acceptance scenarios pass
- [ ] User Story 3: All 4 acceptance scenarios pass
- [ ] User Story 4: All 3 acceptance scenarios pass
- [ ] User Story 5: All 3 acceptance scenarios pass

**Edge Cases (from spec.md)**:
- [ ] Empty search string handled gracefully
- [ ] Special characters in search handled as literal
- [ ] Identical titles during sort use ID as secondary sort
- [ ] No results show clear message
- [ ] Invalid sort/filter options handled with error message
- [ ] Empty task list displays friendly message

**Menu Integration**:
- [ ] Menu displays 8 options correctly
- [ ] Menu validation accepts 1-8, rejects others
- [ ] All handlers called correctly from run_menu()
- [ ] Exit option works from position 8

**Performance (from spec.md)**:
- [ ] Search completes in <3 seconds for 1000 tasks
- [ ] Filter completes in <3 seconds for 1000 tasks
- [ ] Sort completes in <3 seconds for 1000 tasks
- [ ] Combined operations complete in <3 seconds

