# Implementation Plan: Search, Filter, and Sort Capabilities

**Branch**: `002-search-filter-sort` | **Date**: 2026-01-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-search-filter-sort/spec.md`

## Summary

This feature adds search, filter, and sort capabilities to the existing Phase I Todo Application. Users will be able to:
- Search tasks by keyword (title or description, case-insensitive)
- Filter tasks by completion status (All/Pending/Completed)
- Sort tasks by multiple criteria (ID/Title/Status, ascending/descending)
- Combine search and filter operations

**Technical Approach**: Extend existing TodoService with new query methods that operate on in-memory task lists. Add new CLI menu handlers for user interaction. All operations are non-destructive (temporary views), maintaining the original task list order.

## Technical Context

**Language/Version**: Python 3.13+ (per constitution)
**Primary Dependencies**: Python standard library only (per constitution)
**Storage**: In-memory (lists and dictionaries) - no persistence (per constitution)
**Testing**: Manual testing against acceptance scenarios (automated tests optional for Phase II)
**Target Platform**: Windows/Linux/macOS command-line interface
**Project Type**: Single project (src/ at repository root)
**Performance Goals**: <3 seconds for search/filter/sort operations on lists up to 1000 tasks
**Constraints**: O(n) time for search/filter, O(n log n) for sort; <10MB memory overhead
**Scale/Scope**: Extends existing 6-option menu to 8-option menu; adds 3 new service methods and 3 new CLI handlers

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Specification Before Implementation ✅ PASS
- Specification complete: `specs/002-search-filter-sort/spec.md`
- 5 user stories with priorities and acceptance scenarios
- 15 functional requirements defined
- Constitutional amendment approved (v1.1.0) allowing controlled enhancement

### Principle II: Planning Before Coding ✅ PASS
- Implementation plan in progress (this document)
- Research phase will identify all technical decisions
- Design phase will document data models and contracts

### Principle III: Tasks Before Execution ✅ PASS
- Task list will be generated via `/sp.tasks` after planning complete
- Each task will reference specific files and be independently verifiable

### Principle IV: Simplicity Over Complexity ✅ PASS
- Python standard library only (no external dependencies)
- Extends existing architecture (models/services/CLI separation)
- No over-engineering: simple list comprehensions and sorted() for operations
- Clean, readable code following existing patterns

### Principle V: Scope Discipline and Controlled Enhancement ✅ PASS
- Feature approved through SDD workflow (specification → planning → tasks → implementation)
- Constitutional amendment v1.1.0 explicitly allows this enhancement
- Maintains core constraints: no database, no persistence, no GUI
- All operations in-memory only

### Technical Constraints ✅ PASS
- Python 3.13+ ✅
- CLI only (menu-driven) ✅
- In-memory storage only ✅
- Standard library only ✅
- Separation of concerns (models/services/CLI) ✅

### Task Entity Rules ✅ PASS
- No changes to Task model (id, title, description, completed)
- All operations read-only on existing attributes

### CLI Behavior Rules ✅ PASS
- Menu-driven interaction maintained
- Clear prompts for all new operations
- Input validation and graceful error handling
- Continuous loop until exit
- User feedback for all operations

### Quality Standards ✅ PASS
- Clean, readable code with descriptive names
- Small, focused functions (single responsibility)
- No dead code
- Comprehensive docstrings for all new methods

**GATE RESULT**: ✅ ALL GATES PASS - Proceed to Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/002-search-filter-sort/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/
│   └── cli-interface.md # Phase 1 output (to be generated)
├── checklists/
│   └── requirements.md  # Spec validation (complete)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   └── task.py          # NO CHANGES - reuse existing Task model
├── services/
│   ├── __init__.py
│   └── todo_service.py  # MODIFY - add search_tasks(), filter_tasks(), sort_tasks()
└── cli/
    ├── __init__.py
    └── menu.py           # MODIFY - add handlers, update menu display, update validation

tests/
└── unit/                # Optional for Phase II (manual testing for now)

main.py                   # NO CHANGES - entry point unchanged
```

**Structure Decision**: Single project structure maintained from Phase I. All new functionality integrates into existing `src/services/todo_service.py` and `src/cli/menu.py` files. No new files required for core implementation (only documentation artifacts).

## Complexity Tracking

**No constitutional violations** - all gates pass. No complexity justification required.

## Phase 0: Research

### Research Questions

1. **Search Algorithm**: Best approach for case-insensitive substring matching in Python standard library
2. **Filter Implementation**: Efficient list filtering patterns for status-based filtering
3. **Sort Implementation**: Python's sorted() function with custom key functions for multi-criteria sorting
4. **Menu UX**: Best practices for extending CLI menus while maintaining usability
5. **Performance**: Benchmarking O(n) operations on large lists (1000+ tasks)

### Research Output

See [research.md](./research.md) for detailed findings (to be generated).

## Phase 1: Design

### Design Artifacts

1. **data-model.md**: Entity specifications (Task model unchanged, conceptual criteria entities)
2. **contracts/cli-interface.md**: Complete CLI specifications for new menu options
3. **quickstart.md**: Developer guide for implementing search/filter/sort features

### Design Decisions

To be documented in research.md and data-model.md based on Phase 0 findings.

## Phase 2: Tasks

Task breakdown will be generated via `/sp.tasks` command after planning complete. Expected task structure:

- **Phase 1: Service Layer** - Implement search_tasks(), filter_tasks(), sort_tasks() methods
- **Phase 2: CLI Handlers** - Implement handle_search_tasks(), handle_filter_tasks(), handle_sort_tasks()
- **Phase 3: Menu Integration** - Update display_menu(), get_menu_choice(), run_menu() for 8-option menu
- **Phase 4: Polish** - Add docstrings, validate edge cases, update README

## Next Steps

1. ✅ Complete this plan document
2. Generate research.md (Phase 0)
3. Generate data-model.md, contracts/, quickstart.md (Phase 1)
4. Run `/sp.tasks` to generate task breakdown (Phase 2)
5. Run `/sp.implement` to execute implementation

---

**Plan Status**: Ready for Phase 0 research
**Next Command**: Continue with research.md generation
