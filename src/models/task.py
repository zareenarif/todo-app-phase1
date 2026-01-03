"""
Task Model - Represents a todo item

Adheres to constitutional Task Entity Rules:
- id: Integer, auto-incremented, unique, immutable
- title: String, required, non-empty
- description: String, optional
- completed: Boolean, default False
"""


class Task:
    """
    Represents a todo task item.

    Attributes:
        id (int): Unique task identifier (immutable)
        title (str): Task title (required, non-empty)
        description (str): Optional task description
        completed (bool): Completion status (default: False)
    """

    def __init__(self, task_id, title, description=None, completed=False):
        """
        Initialize a new Task.

        Args:
            task_id (int): Unique integer identifier
            title (str): Task title (must be non-empty after strip)
            description (str, optional): Optional description
            completed (bool, optional): Completion status (default: False)

        Raises:
            ValueError: If title is empty after stripping whitespace
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        self._id = task_id  # Immutable (no setter, private attribute)
        self.title = title.strip()
        self.description = description.strip() if description else None
        self.completed = completed

    @property
    def id(self):
        """Get task ID (immutable)."""
        return self._id

    def __repr__(self):
        """String representation for debugging."""
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"

    def __str__(self):
        """Human-readable string representation."""
        status = "Completed" if self.completed else "Pending"
        return f"[{self.id}] {self.title} - {status}"
