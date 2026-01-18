"""
Complex class example for multi-path assessment testing.

This demonstrates object-oriented design, error handling,
and data structures. Good for testing TECHNICAL, DESIGN,
and COLLABORATION paths.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    """Represents a single task in the system."""

    id: int
    title: str
    description: str
    created_at: datetime
    completed: bool = False


class TaskManager:
    """
    Manages a collection of tasks with CRUD operations.

    This class provides a simple interface for managing tasks,
    including creation, retrieval, updating, and deletion.
    """

    def __init__(self):
        """Initialize an empty task manager."""
        self.tasks: List[Task] = []
        self._next_id = 1

    def create_task(self, title: str, description: str) -> Task:
        """
        Create a new task.

        Args:
            title: The task title
            description: Detailed description of the task

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title or description is empty
        """
        if not title or not description:
            raise ValueError("Title and description cannot be empty")

        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            created_at=datetime.now(),
        )
        self.tasks.append(task)
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id: The unique task identifier

        Returns:
            The Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> bool:
        """
        Mark a task as completed.

        Args:
            task_id: The unique task identifier

        Returns:
            True if task was found and marked complete, False otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.completed = True
            return True
        return False

    def list_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        """
        List all tasks, optionally filtered by completion status.

        Args:
            completed: If True, return only completed tasks.
                      If False, return only incomplete tasks.
                      If None, return all tasks.

        Returns:
            List of Task objects matching the filter
        """
        if completed is None:
            return self.tasks.copy()
        return [task for task in self.tasks if task.completed == completed]


# Example usage
if __name__ == "__main__":
    manager = TaskManager()

    # Create some tasks
    task1 = manager.create_task("Review PR", "Review the new authentication PR")
    task2 = manager.create_task("Fix bug", "Fix the memory leak in task processor")
    task3 = manager.create_task("Write docs", "Document the new API endpoints")

    # Complete one task
    manager.complete_task(task1.id)

    # List tasks
    print("All tasks:", len(manager.list_tasks()))
    print("Completed:", len(manager.list_tasks(completed=True)))
    print("Incomplete:", len(manager.list_tasks(completed=False)))
