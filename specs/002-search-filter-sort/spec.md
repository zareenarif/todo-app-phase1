# Feature Specification: Search, Filter, and Sort Capabilities

**Feature Branch**: `002-search-filter-sort`
**Created**: 2026-01-03
**Status**: Draft
**Input**: User description: "add in choice option 'search/filter tasks' and 'sort tasks' options in todo app"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Search Tasks by Keyword (Priority: P1)

As a user, I want to search for tasks by entering keywords so that I can quickly find specific tasks without scrolling through the entire list.

**Why this priority**: Search is the most fundamental discovery feature. Users with many tasks need a quick way to locate specific items. This is the MVP for enhanced task discovery.

**Independent Test**: Can be fully tested by adding 10+ tasks with distinct titles, selecting "Search Tasks" from menu, entering a keyword, and verifying only matching tasks appear. Delivers immediate value for users with large task lists.

**Acceptance Scenarios**:

1. **Given** I have tasks with titles "Buy groceries", "Buy books", "Read email", **When** I search for "buy", **Then** I see only "Buy groceries" and "Buy books" in results
2. **Given** I have tasks with varying titles, **When** I search for a keyword that matches no tasks, **Then** I see message "No tasks found matching '[keyword]'"
3. **Given** I have tasks with descriptions, **When** I search for a keyword in a task description, **Then** I see tasks where keyword appears in title OR description
4. **Given** I search for a task, **When** I view search results, **Then** I see task ID, title, and completion status (same format as View All Tasks)

---

### User Story 2 - Filter Tasks by Completion Status (Priority: P1)

As a user, I want to filter tasks to show only completed or only pending tasks so that I can focus on what needs to be done or review what I've accomplished.

**Why this priority**: Filtering by status is essential for task management. Users need to see pending work separately from completed items. This is co-MVP with search.

**Independent Test**: Can be fully tested by creating mix of completed and pending tasks, selecting "Filter Tasks" from menu, choosing "Pending only", and verifying only incomplete tasks appear. Delivers immediate value for focus and productivity.

**Acceptance Scenarios**:

1. **Given** I have 5 pending and 3 completed tasks, **When** I filter by "Pending only", **Then** I see exactly 5 tasks with status "Pending"
2. **Given** I have 5 pending and 3 completed tasks, **When** I filter by "Completed only", **Then** I see exactly 3 tasks with status "Completed"
3. **Given** I have 5 pending and 3 completed tasks, **When** I filter by "All tasks", **Then** I see all 8 tasks
4. **Given** I filter by "Pending only" and no pending tasks exist, **When** results are displayed, **Then** I see "No pending tasks found"

---

### User Story 3 - Sort Tasks by Different Criteria (Priority: P2)

As a user, I want to sort tasks by ID, title, or completion status so that I can organize my task list according to my current needs.

**Why this priority**: Sorting provides additional organization but isn't required for basic discovery. Users can still function with search/filter alone. This enhances the experience once discovery basics are in place.

**Independent Test**: Can be fully tested by creating tasks in random order with varying titles and statuses, selecting "Sort Tasks" from menu, choosing a sort criterion, and verifying tasks appear in correct order. Delivers value for users who need specific organization.

**Acceptance Scenarios**:

1. **Given** I have tasks with IDs 1, 3, 5, 2, 4 (after some deletions and adds), **When** I sort by "ID (ascending)", **Then** tasks appear in order: 1, 2, 3, 4, 5
2. **Given** I have tasks titled "Zebra", "Apple", "Mango", **When** I sort by "Title (A-Z)", **Then** tasks appear in order: Apple, Mango, Zebra
3. **Given** I have mixed completed and pending tasks, **When** I sort by "Status (completed first)", **Then** all completed tasks appear before pending tasks
4. **Given** I have mixed completed and pending tasks, **When** I sort by "Status (pending first)", **Then** all pending tasks appear before completed tasks

---

### User Story 4 - Combine Search and Filter (Priority: P2)

As a user, I want to apply both search keywords and status filters together so that I can find specific tasks within a particular completion state.

**Why this priority**: Combined operations provide power-user functionality. Most users can function with search OR filter independently. This is valuable for advanced organization but not required for basic use.

**Independent Test**: Can be fully tested by creating diverse task set, applying search keyword AND status filter, and verifying only tasks matching BOTH criteria appear. Delivers value for users managing complex task lists.

**Acceptance Scenarios**:

1. **Given** I have "Buy groceries" (pending), "Buy books" (completed), "Read email" (pending), **When** I search for "buy" AND filter by "Pending only", **Then** I see only "Buy groceries"
2. **Given** I have multiple tasks, **When** I search for "meeting" AND filter by "Completed only", **Then** I see only completed tasks containing "meeting"
3. **Given** I apply search and filter, **When** no tasks match both criteria, **Then** I see "No tasks found matching '[keyword]' with status '[filter]'"

---

### User Story 5 - Clear Search/Filter/Sort Settings (Priority: P3)

As a user, I want to easily return to viewing all tasks in original order so that I can reset any applied search, filter, or sort operations.

**Why this priority**: This is a convenience feature. Users can always restart the app to reset views, or manually select "All tasks" filter. Nice to have but not essential for core functionality.

**Independent Test**: Can be fully tested by applying various search/filter/sort operations, then selecting "Clear all filters" or "View all tasks", and verifying original task list appears in creation order. Delivers convenience but not critical value.

**Acceptance Scenarios**:

1. **Given** I have search keyword "buy" and filter "Pending" applied, **When** I select "Clear filters", **Then** I see all tasks in original creation order
2. **Given** I have sorted tasks by title, **When** I select "View all tasks", **Then** I see all tasks in original ID order (creation order)
3. **Given** No filters are applied, **When** I select "Clear filters", **Then** I see message "No filters currently applied" and task list unchanged

---

### Edge Cases

- What happens when user searches for empty string or whitespace-only? → Treat as "show all tasks"
- What happens when search keyword contains special characters? → Perform literal string matching (no regex interpretation)
- What happens when tasks have identical titles during alphabetical sort? → Use ID as secondary sort (stable sort)
- What happens when combining search/filter/sort and no tasks match? → Show clear "No tasks found" message with applied criteria
- What happens when user enters invalid sort option? → Show error "Invalid sort option. Please try again."
- What happens when displaying very long task titles in filtered/sorted views? → Truncate to 30 characters (consistent with existing View Tasks behavior)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to search tasks by keyword matching against title OR description (case-insensitive)
- **FR-002**: System MUST allow users to filter tasks by completion status (Pending only, Completed only, All tasks)
- **FR-003**: System MUST allow users to sort tasks by ID (ascending/descending), Title (A-Z/Z-A), or Status (completed first/pending first)
- **FR-004**: System MUST preserve original task list and apply search/filter/sort as temporary views (non-destructive operations)
- **FR-005**: System MUST display search/filter/sort results using same table format as "View Tasks" (ID | Title | Status)
- **FR-006**: System MUST show result count after search/filter operations (e.g., "Found 3 tasks matching 'buy'")
- **FR-007**: System MUST allow combining search keyword with status filter in single operation
- **FR-008**: System MUST handle empty search results gracefully with clear messaging
- **FR-009**: System MUST perform case-insensitive keyword matching for search
- **FR-010**: System MUST maintain immutability of original task order (ID-based creation order)
- **FR-011**: System MUST add new menu options: "Search Tasks" (option 7), "Filter Tasks" (option 8), "Sort Tasks" (option 9)
- **FR-012**: System MUST update "Exit" option to menu position 10 (currently option 6)
- **FR-013**: System MUST validate menu input range 1-10 instead of 1-6
- **FR-014**: System MUST return to main menu after each search/filter/sort operation (not persistent views)
- **FR-015**: Users MUST be able to perform search/filter/sort operations on empty task list without errors (show "No tasks found")

### Key Entities

- **Task**: No changes to existing entity (id, title, description, completed) - search/filter/sort operate on existing data
- **SearchCriteria** (conceptual): Keyword string, case-insensitive matching, applies to title and description fields
- **FilterCriteria** (conceptual): Status filter (all/pending/completed), applies to completed boolean field
- **SortCriteria** (conceptual): Sort field (id/title/status), sort direction (ascending/descending)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can search for tasks and see results in under 3 seconds (for lists up to 1000 tasks)
- **SC-002**: Search matches are accurate (100% of tasks containing keyword in title or description appear in results)
- **SC-003**: Filter operations correctly separate tasks (0% error rate in status filtering)
- **SC-004**: Sort operations produce correct ordering (100% accurate alphabetical/numerical/status sorting)
- **SC-005**: All search/filter/sort operations are non-destructive (original task list unchanged after operations)
- **SC-006**: Empty search results display friendly message (no crashes or blank screens)
- **SC-007**: Menu remains intuitive with additional options (users can navigate without confusion)

## Technical Constraints *(from constitution)*

### Constitutional Compliance

**NOTE**: This feature expands functionality beyond Phase I scope. Phase I explicitly limited features to basic CRUD operations. This specification requires constitutional amendment or explicit override to proceed.

**Constitution Principle V - Scope Limitation**:
- Original: "This is Phase I - intentionally simple. Do not add features not explicitly listed."
- **Proposed Amendment**: "Features may be added through proper SDD workflow (specification → planning → tasks → implementation) with explicit user approval."

**All other constitutional principles remain enforced**:
- ✅ Python 3.13+ standard library only (no external dependencies required)
- ✅ In-memory storage (search/filter/sort operate on existing in-memory task lists)
- ✅ CLI interface only (menu-driven interaction maintained)
- ✅ Separation of concerns (services layer handles logic, CLI handles display)
- ✅ Clean, readable code with comprehensive docstrings

## Assumptions & Dependencies

### Assumptions

1. Search is case-insensitive (user expectation for usability)
2. Empty keyword matches all tasks (sensible default behavior)
3. Original task list maintains creation order by ID
4. Search/filter/sort are temporary views, not persistent (maintains simplicity)
5. All operations return to main menu (no nested menus or state)

### Dependencies

- Existing TodoService class (src/services/todo_service.py) will require new methods
- Existing menu.py (src/cli/menu.py) will require new handlers and menu updates
- No new external dependencies required (Python standard library sufficient)
- No changes to Task model (src/models/task.py) required

## Out of Scope *(Phase II candidates)*

- Persistent search/filter preferences (would require storage)
- Advanced search operators (AND/OR/NOT logic)
- Regular expression pattern matching
- Search history or saved searches
- Multi-field sort (primary + secondary sort keys)
- Custom sort orders or user-defined criteria
- Real-time search (as-you-type filtering)
- Search result highlighting or emphasizing matches

## Integration Notes

### Menu Changes Required

Current menu (6 options):
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Proposed menu (10 options):
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Search Tasks *(new)*
7. Filter Tasks *(new)*
8. Sort Tasks *(new)*
9. Advanced: Search + Filter *(new)*
10. Exit *(moved from position 6)*

Alternative simplified menu (8 options):
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Search/Filter Tasks *(combined new option)*
7. Sort Tasks *(new)*
8. Exit *(moved from position 6)*

**Recommendation**: Start with simplified 8-option menu for Phase II. Can expand to 10 options in later phase if user feedback indicates need for separation.

## Non-Functional Requirements

### Performance

- Search operations complete in O(n) time where n = number of tasks
- Filter operations complete in O(n) time
- Sort operations complete in O(n log n) time
- All operations acceptable for lists up to 10,000 tasks on standard hardware

### Usability

- Search prompts clearly indicate "Enter keyword (searches title and description):"
- Filter prompts provide numbered options: 1=All, 2=Pending, 3=Completed
- Sort prompts provide numbered options with clear descriptions
- Result counts always displayed: "Found X tasks" or "Showing X of Y total tasks"

### Reliability

- Invalid menu choices handled gracefully (same pattern as existing validation)
- Empty task lists handled without errors
- Special characters in search terms handled as literal strings
- Very long search keywords (>100 chars) accepted but may not match anything

---

**Specification Status**: Ready for planning phase
**Next Step**: Run `/sp.plan` to generate implementation plan
