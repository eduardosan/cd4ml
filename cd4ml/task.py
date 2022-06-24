import inspect


class Task:
    """Generic task to be run in a pipeline."""

    def __init__(self, name, description=None, task=None):
        """
        :param name: Task name to be shown on later DAG
        :param description: Task human description
        :param task: Function to be called in this task
        """
        self.name = name
        self.description = description
        if self.description is None:
            self.description = name

        self.params = []
        self.task = task

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, value):
        """Get parameters from task"""
        if value is not None:
            sig = inspect.signature(value)
            self.params = sig.parameters
            self._task = value

    def run(self, *args, **kwargs):
        """Run method task if defined"""
        return self.task(*args, **kwargs)
