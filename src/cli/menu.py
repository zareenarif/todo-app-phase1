"""
CLI Menu - Command-line interface for todo application

Provides menu-driven interaction with numbered options and graceful error handling.
"""

from src.services.todo_service import TodoService


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
    print("6. Search/Filter Tasks")
    print("7. Sort Tasks")
    print("8. Exit")
    print()


def get_menu_choice():
    """
    Get and validate user menu choice.

    Returns:
        int or None: Valid choice (1-8) or None if invalid
    """
    try:
        choice = input("Enter your choice (1-8): ").strip()
        choice_num = int(choice)
        if 1 <= choice_num <= 8:
            return choice_num
        else:
            print("\n✗ Error: Invalid choice. Please enter a number between 1 and 8.")
            return None
    except ValueError:
        print("\n✗ Error: Invalid choice. Please enter a number between 1 and 8.")
        return None


def validate_integer_input(prompt):
    """
    Validate integer input from user.

    Args:
        prompt (str): Input prompt message

    Returns:
        int or None: Valid integer or None if invalid
    """
    try:
        value = input(prompt).strip()
        return int(value)
    except ValueError:
        print("\n✗ Error: Invalid task ID. Please enter a number.")
        return None


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


def handle_add_task(service):
    """
    Handle adding a new task.

    Args:
        service (TodoService): Todo service instance
    """
    print("\n" + "=" * 30)
    print("=== Add Task ===")
    print("=" * 30)

    title = input("\nEnter task title: ").strip()
    if not title:
        print("\n✗ Error: Task title cannot be empty.")
        return

    description = input("Enter task description (optional, press Enter to skip): ").strip()
    if not description:
        description = None

    try:
        task = service.add_task(title, description)
        print("\n✓ Task added successfully!")
        print(f"  ID: {task.id}")
        print(f"  Title: {task.title}")
        print(f"  Description: {task.description if task.description else 'None'}")
        print(f"  Status: Pending")
    except ValueError as e:
        print(f"\n✗ Error: {e}")


def handle_view_tasks(service):
    """
    Handle viewing all tasks.

    Args:
        service (TodoService): Todo service instance
    """
    print("\n" + "=" * 30)
    print("=== All Tasks ===")
    print("=" * 30)
    print()

    tasks = service.get_all_tasks()

    if not tasks:
        print("No tasks found. Add a task to get started!")
        return

    # Display table header
    print(f"{'ID':<5} | {'Title':<30} | {'Status'}")
    print("-" * 50)

    # Display tasks
    for task in tasks:
        status = "Completed" if task.completed else "Pending"
        # Truncate long titles for display
        title_display = task.title[:30] if len(task.title) > 30 else task.title
        print(f"{task.id:<5} | {title_display:<30} | {status}")

    print(f"\nTotal: {len(tasks)} task{'s' if len(tasks) != 1 else ''}")


def handle_update_task(service):
    """
    Handle updating an existing task.

    Args:
        service (TodoService): Todo service instance
    """
    print("\n" + "=" * 30)
    print("=== Update Task ===")
    print("=" * 30)
    print()

    task_id = validate_integer_input("Enter task ID to update: ")
    if task_id is None:
        return

    task = service.get_task_by_id(task_id)
    if not task:
        print(f"\n✗ Error: Task with ID {task_id} not found.")
        return

    # Show current values
    print(f"\nCurrent title: {task.title}")
    new_title = input("Enter new title (press Enter to keep current): ").strip()

    print(f"Current description: {task.description if task.description else 'None'}")
    new_description = input("Enter new description (press Enter to keep current): ").strip()

    # Update only if values provided
    update_title = new_title if new_title else None
    update_description = new_description if new_description else None

    if update_title is None and update_description is None:
        print("\nNo changes made.")
        return

    success, message = service.update_task(task_id, update_title, update_description)

    if success:
        print(f"\n✓ {message}!")
        updated_task = service.get_task_by_id(task_id)
        print(f"  ID: {updated_task.id}")
        print(f"  Title: {updated_task.title}")
        print(f"  Description: {updated_task.description if updated_task.description else 'None'}")
        status = "Completed" if updated_task.completed else "Pending"
        print(f"  Status: {status}")
    else:
        print(f"\n✗ Error: {message}")


def handle_delete_task(service):
    """
    Handle deleting a task.

    Args:
        service (TodoService): Todo service instance
    """
    print("\n" + "=" * 30)
    print("=== Delete Task ===")
    print("=" * 30)
    print()

    task_id = validate_integer_input("Enter task ID to delete: ")
    if task_id is None:
        return

    task = service.get_task_by_id(task_id)
    if not task:
        print(f"\n✗ Error: Task with ID {task_id} not found.")
        return

    # Confirm deletion
    confirmation = input(f"\nAre you sure you want to delete task \"{task.title}\"? (y/n): ").strip().lower()

    if confirmation in ['y', 'yes']:
        success, message = service.delete_task(task_id)
        if success:
            print(f"\n✓ {message}!")
        else:
            print(f"\n✗ Error: {message}")
    else:
        print("\nDelete cancelled.")


def handle_toggle_completion(service):
    """
    Handle toggling task completion status.

    Args:
        service (TodoService): Todo service instance
    """
    print("\n" + "=" * 30)
    print("=== Mark Task Complete/Incomplete ===")
    print("=" * 30)
    print()

    task_id = validate_integer_input("Enter task ID: ")
    if task_id is None:
        return

    success, message, new_status = service.toggle_task_completion(task_id)

    if success:
        task = service.get_task_by_id(task_id)
        status_text = "Completed" if new_status else "Pending"
        print(f"\n✓ Task marked as {status_text.lower()}!")
        print(f"  ID: {task.id}")
        print(f"  Title: {task.title}")
        print(f"  Status: {status_text}")
    else:
        print(f"\n✗ Error: {message}")


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

    # Display table
    print(f"{'ID':<5} | {'Title':<30} | {'Status'}")
    print("-" * 50)

    for task in results:
        status = "Completed" if task.completed else "Pending"
        title_display = task.title[:30] if len(task.title) > 30 else task.title
        print(f"{task.id:<5} | {title_display:<30} | {status}")

    print(f"\nTotal: {len(results)} task{'s' if len(results) != 1 else ''}")


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


def handle_exit():
    """
    Handle application exit.

    Returns:
        bool: True to signal exit
    """
    print("\nGoodbye! All tasks have been cleared.")
    return True


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
            handle_search_filter_tasks(service)
        elif choice == 7:
            handle_sort_tasks(service)
        elif choice == 8:
            exit_requested = handle_exit()
