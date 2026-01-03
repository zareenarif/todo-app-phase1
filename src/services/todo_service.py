"""
TodoService - Business logic for todo task management

Provides CRUD operations for tasks with in-memory storage.
Uses dual storage: list for ordered display, dict for O(1) lookup.
"""

from src.models.task import Task


class TodoService:
    """
    Service layer for todo task management.

    Maintains tasks in memory using:
    - List for ordered display
    - Dictionary for fast lookup by ID

    Attributes:
        _tasks (list): Ordered list of tasks
        _task_dict (dict): ID to task mapping for O(1) lookup
        _next_id (int): Counter for auto-incrementing task IDs
    """

    def __init__(self):
        """Initialize TodoService with empty task storage."""
        self._tasks = []
        self._task_dict = {}
        self._next_id = 1

    def add_task(self, title, description=None):
        """
        Add a new task.

        Args:
            title (str): Task title (required, non-empty)
            description (str, optional): Task description

        Returns:
            Task: The created task

        Raises:
            ValueError: If title is empty
        """
        task = Task(self._next_id, title, description, False)
        self._tasks.append(task)
        self._task_dict[task.id] = task
        self._next_id += 1
        return task

    def get_all_tasks(self):
        """
        Get all tasks.

        Returns:
            list: List of all tasks in creation order
        """
        return self._tasks.copy()

    def get_task_by_id(self, task_id):
        """
        Get task by ID.

        Args:
            task_id (int): Task ID

        Returns:
            Task or None: Task if found, None otherwise
        """
        return self._task_dict.get(task_id)

    def update_task(self, task_id, title=None, description=None):
        """
        Update task title and/or description.

        Args:
            task_id (int): Task ID
            title (str, optional): New title (must be non-empty if provided)
            description (str, optional): New description

        Returns:
            tuple: (success: bool, message: str)
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False, f"Task with ID {task_id} not found"

        if title is not None:
            if not title or not title.strip():
                return False, "Task title cannot be empty"
            task.title = title.strip()

        if description is not None:
            task.description = description.strip() if description else None

        return True, "Task updated successfully"

    def delete_task(self, task_id):
        """
        Delete task by ID.

        Args:
            task_id (int): Task ID

        Returns:
            tuple: (success: bool, message: str)
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False, f"Task with ID {task_id} not found"

        self._tasks.remove(task)
        del self._task_dict[task_id]
        return True, "Task deleted successfully"

    def toggle_task_completion(self, task_id):
        """
        Toggle task completion status.

        Args:
            task_id (int): Task ID

        Returns:
            tuple: (success: bool, message: str, new_status: bool or None)
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False, f"Task with ID {task_id} not found", None

        task.completed = not task.completed
        status_text = "completed" if task.completed else "pending"
        return True, f"Task marked as {status_text}", task.completed

    def search_tasks(self, keyword):
        """
        Search tasks by keyword in title or description.

        Args:
            keyword (str): Search term (case-insensitive)

        Returns:
            list: Tasks matching keyword in title or description
        """
        if not keyword or not keyword.strip():
            return self._tasks.copy()

        keyword_lower = keyword.lower().strip()
        results = [
            task for task in self._tasks
            if keyword_lower in task.title.lower() or
               (task.description and keyword_lower in task.description.lower())
        ]
        return results

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
            return sorted(self._tasks, key=lambda t: t.completed, reverse=reverse)
        else:
            return self._tasks.copy()  # Invalid sort returns original order
