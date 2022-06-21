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

        self.task = task

    def run(self, *args, **kwargs):
        """Run method task if defined"""
        return self.task(*args, **kwargs)
