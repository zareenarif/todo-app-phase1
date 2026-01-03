# CLI Interface Contract: Phase I Todo Application

**Feature**: 001-todo-app
**Date**: 2026-01-03
**Interface Type**: Command Line Interface (CLI)
**Status**: Complete

## Overview

This document defines the contract for the Command Line Interface of the Phase I Todo Application. It specifies exact input/output formats, menu options, prompts, and error messages that users will interact with.

## Application Entry Point

### Command
```bash
python main.py
# or
python3 main.py
```

### Startup Behavior
1. Application launches immediately (< 2 seconds)
2. Displays main menu
3. Waits for user input
4. No configuration or setup required

### Exit Codes
- `0`: Normal exit (user selected Exit)
- `1`: Error exit (unexpected error, though should not occur per constitution)

## Main Menu Interface

### Menu Display

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

**Display Rules**:
- Menu title centered or left-aligned: `=== Todo Application ===`
- Blank line after title
- Numbered options 1-6
- Blank line before prompt
- Prompt text: `Enter your choice (1-6): `
- Cursor waits for input after prompt

### Menu Input Contract

**Valid Inputs**:
- Single digit: `1`, `2`, `3`, `4`, `5`, or `6`
- May include leading/trailing whitespace (stripped before validation)

**Invalid Inputs**:
- Numbers outside range: `0`, `7`, `99`, `-1`
- Non-numeric input: `a`, `abc`, `one`, `!@#`
- Empty input (just Enter key)

**Invalid Input Handling**:
```
Invalid choice. Please enter a number between 1 and 6.

[Menu redisplays]
```

## Operation 1: Add Task

### Prompt Sequence

```
=== Add Task ===

Enter task title: _
```

**After title entry**:
```
Enter task description (optional, press Enter to skip): _
```

### Input Contracts

#### Title Input
- **Required**: Yes
- **Validation**: Non-empty after whitespace strip
- **Max length**: No limit (system memory)
- **Invalid inputs**:
  - Empty string `""`
  - Whitespace-only `"   "`

#### Description Input
- **Required**: No
- **Validation**: None (any string accepted)
- **Max length**: No limit
- **Optional indicator**: User can press Enter to skip

### Success Response

```
✓ Task added successfully!
  ID: 1
  Title: Buy groceries
  Description: None
  Status: Pending

[Return to main menu]
```

**Success Response Format**:
- Checkmark symbol (✓) or similar indicator
- Display assigned task ID
- Display entered title
- Display description (or "None" if not provided)
- Status: always "Pending" for new tasks

### Error Response (Empty Title)

```
✗ Error: Task title cannot be empty.

[Return to Add Task prompts or main menu]
```

### Example Interactions

#### Valid: Title Only
```
Enter task title: Buy groceries
Enter task description (optional, press Enter to skip):

✓ Task added successfully!
  ID: 1
  Title: Buy groceries
  Description: None
  Status: Pending
```

#### Valid: Title and Description
```
Enter task title: Fix bug
Enter task description (optional, press Enter to skip): Update validation logic

✓ Task added successfully!
  ID: 2
  Title: Fix bug
  Description: Update validation logic
  Status: Pending
```

#### Invalid: Empty Title
```
Enter task title:
✗ Error: Task title cannot be empty.
```

## Operation 2: View Tasks

### Display Format (Tasks Exist)

```
=== All Tasks ===

ID | Title              | Status
-----------------------------------------
1  | Buy groceries      | Pending
2  | Fix bug            | Completed
3  | Write report       | Pending

Total: 3 tasks

[Return to main menu]
```

**Column Specifications**:
- **ID**: Left-aligned integer
- **Title**: Left-aligned string (may truncate if very long for display)
- **Status**: "Pending" or "Completed"

**Header**:
- Column names: `ID | Title | Status`
- Separator line of dashes

**Footer**:
- Total count: `Total: {n} tasks`

### Display Format (No Tasks)

```
=== All Tasks ===

No tasks found. Add a task to get started!

[Return to main menu]
```

### Example Interactions

#### Empty List
```
=== All Tasks ===

No tasks found. Add a task to get started!
```

#### With Tasks
```
=== All Tasks ===

ID | Title              | Status
-----------------------------------------
1  | Buy groceries      | Pending
2  | Fix bug            | Completed

Total: 2 tasks
```

## Operation 3: Update Task

### Prompt Sequence

```
=== Update Task ===

Enter task ID to update: _
```

**If ID is valid**:
```
Current title: Buy groceries
Enter new title (press Enter to keep current): _
```

**After title entry**:
```
Current description: None
Enter new description (press Enter to keep current): _
```

### Input Contracts

#### Task ID Input
- **Type**: Integer
- **Validation**: Must exist in current tasks
- **Error cases**:
  - Non-integer: `"abc"`, `"1.5"`
  - Non-existent ID: `999`

#### New Title Input
- **Required**: No (can keep current by pressing Enter)
- **Validation**: If provided, must be non-empty after strip
- **Empty input**: Keeps current title

#### New Description Input
- **Required**: No (can keep current by pressing Enter)
- **Validation**: None
- **Empty input**: Keeps current description

### Success Response

```
✓ Task updated successfully!
  ID: 1
  Title: Buy milk and groceries
  Description: Weekly shopping
  Status: Pending

[Return to main menu]
```

### Error Responses

#### Invalid ID Format
```
✗ Error: Invalid task ID. Please enter a number.

[Return to main menu]
```

#### Task Not Found
```
✗ Error: Task with ID 999 not found.

[Return to main menu]
```

#### Empty Title on Update
```
✗ Error: Task title cannot be empty.

[Return to Update Task prompts or main menu]
```

### Example Interactions

#### Update Title Only
```
Enter task ID to update: 1

Current title: Buy groceries
Enter new title (press Enter to keep current): Buy milk and groceries

Current description: None
Enter new description (press Enter to keep current):

✓ Task updated successfully!
  ID: 1
  Title: Buy milk and groceries
  Description: None
  Status: Pending
```

#### Update Both Fields
```
Enter task ID to update: 1

Current title: Buy groceries
Enter new title (press Enter to keep current): Buy milk and groceries

Current description: None
Enter new description (press Enter to keep current): Weekly shopping

✓ Task updated successfully!
  ID: 1
  Title: Buy milk and groceries
  Description: Weekly shopping
  Status: Pending
```

#### Task Not Found
```
Enter task ID to update: 999

✗ Error: Task with ID 999 not found.
```

## Operation 4: Delete Task

### Prompt Sequence

```
=== Delete Task ===

Enter task ID to delete: _
```

**After ID entry (if valid)**:
```
Are you sure you want to delete task "Buy groceries"? (y/n): _
```

### Input Contracts

#### Task ID Input
- **Type**: Integer
- **Validation**: Must exist in current tasks
- **Error cases**: Same as Update Task

#### Confirmation Input
- **Type**: String (case-insensitive)
- **Valid inputs**:
  - Confirm: `y`, `Y`, `yes`, `Yes`, `YES`
  - Cancel: `n`, `N`, `no`, `No`, `NO`
- **Behavior**:
  - Confirmed: Delete task
  - Cancelled: Return to main menu without deleting

### Success Response

```
✓ Task deleted successfully!

[Return to main menu]
```

### Cancellation Response

```
Delete cancelled.

[Return to main menu]
```

### Error Responses

#### Task Not Found
```
✗ Error: Task with ID 999 not found.

[Return to main menu]
```

### Example Interactions

#### Successful Deletion
```
Enter task ID to delete: 1

Are you sure you want to delete task "Buy groceries"? (y/n): y

✓ Task deleted successfully!
```

#### Cancelled Deletion
```
Enter task ID to delete: 1

Are you sure you want to delete task "Buy groceries"? (y/n): n

Delete cancelled.
```

#### Task Not Found
```
Enter task ID to delete: 999

✗ Error: Task with ID 999 not found.
```

## Operation 5: Mark Task Complete/Incomplete

### Prompt Sequence

```
=== Mark Task Complete/Incomplete ===

Enter task ID: _
```

### Input Contracts

#### Task ID Input
- **Type**: Integer
- **Validation**: Must exist in current tasks
- **Error cases**: Same as Update Task

### Success Response (Marked Complete)

```
✓ Task marked as completed!
  ID: 1
  Title: Buy groceries
  Status: Completed

[Return to main menu]
```

### Success Response (Marked Incomplete)

```
✓ Task marked as pending!
  ID: 1
  Title: Buy groceries
  Status: Pending

[Return to main menu]
```

**Toggle Behavior**:
- If current status is Pending → change to Completed
- If current status is Completed → change to Pending

### Error Response

#### Task Not Found
```
✗ Error: Task with ID 999 not found.

[Return to main menu]
```

### Example Interactions

#### Toggle to Completed
```
Enter task ID: 1

✓ Task marked as completed!
  ID: 1
  Title: Buy groceries
  Status: Completed
```

#### Toggle to Pending
```
Enter task ID: 1

✓ Task marked as pending!
  ID: 1
  Title: Buy groceries
  Status: Pending
```

## Operation 6: Exit

### Behavior
1. User selects option 6
2. Application displays goodbye message
3. Application terminates with exit code 0

### Exit Message

```
Goodbye! All tasks have been cleared.
```

**Note**: Reminds user that data is not persisted (Phase I constraint)

### Example Interaction

```
Enter your choice (1-6): 6

Goodbye! All tasks have been cleared.

[Application exits]
```

## Input Validation Standards

### General Principles
1. **Never crash**: All invalid input must be handled gracefully
2. **Clear errors**: Error messages must explain what went wrong
3. **Immediate feedback**: Display errors immediately after invalid input
4. **Return to context**: After errors, return to appropriate menu/prompt

### Numeric Input Validation

```python
try:
    choice = int(input("Enter your choice (1-6): "))
    if choice < 1 or choice > 6:
        print("Invalid choice. Please enter a number between 1 and 6.")
except ValueError:
    print("Invalid choice. Please enter a number between 1 and 6.")
```

### String Input Validation (Title)

```python
title = input("Enter task title: ").strip()
if not title:
    print("✗ Error: Task title cannot be empty.")
```

## Error Message Format

**Standard Format**:
```
✗ Error: {specific error message}
```

**Error Symbol**: `✗` or `Error:` prefix
**Message**: Clear, actionable description

**Standard Error Messages**:
- `"Task title cannot be empty."`
- `"Invalid task ID. Please enter a number."`
- `"Task with ID {id} not found."`
- `"Invalid choice. Please enter a number between 1 and 6."`

## Success Message Format

**Standard Format**:
```
✓ {operation} successfully!
  [Optional details]
```

**Success Symbol**: `✓` or similar
**Message**: Confirms operation completed

**Standard Success Messages**:
- `"Task added successfully!"`
- `"Task updated successfully!"`
- `"Task deleted successfully!"`
- `"Task marked as completed!"`
- `"Task marked as pending!"`

## Display Conventions

### Headers
- Section headers use `===` delimiter
- Format: `=== {Section Name} ===`
- Examples: `=== Todo Application ===`, `=== Add Task ===`

### Spacing
- Blank line before and after headers
- Blank line before prompts
- Blank line between menu and next display

### Status Display
- Pending tasks: `Pending`
- Completed tasks: `Completed`
- Case-sensitive, first letter capitalized

### Symbols
- Success: `✓` (checkmark) or `[OK]`
- Error: `✗` (X mark) or `[ERROR]`
- Info: `-` or `*`

## Accessibility Considerations

1. **Plain text**: All output in plain text (no colors/formatting dependencies)
2. **Screen reader friendly**: Use clear labels and structure
3. **Keyboard only**: All operations via keyboard input
4. **Clear prompts**: Every input has explicit prompt
5. **Error clarity**: Errors explain what's wrong and what to do

## Character Encoding

- **Encoding**: UTF-8
- **Symbols**: Use ASCII-safe alternatives if UTF-8 symbols fail
  - ✓ → [OK] or (done)
  - ✗ → [X] or (error)

## Performance Contracts

Per success criteria:
- **Response time**: < 1 second for all operations
- **Startup time**: < 2 seconds
- **Display time**: < 1 second for viewing up to 1000 tasks

## Contract Validation

This interface contract is validated by:
1. Functional requirements FR-010 through FR-015 in spec.md
2. CLI Behavior Rules in constitution.md
3. User story acceptance scenarios in spec.md

## Changes from Specification

None. This contract directly implements the specification requirements with no deviations.

## References

1. Feature Specification: `specs/001-todo-app/spec.md`
2. Constitution CLI Behavior Rules: `.specify/memory/constitution.md` (lines 104-112)
3. Functional Requirements: FR-010 through FR-015
