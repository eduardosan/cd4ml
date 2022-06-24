from cd4ml.task import Task


class LocalExecutor:
    """Local executor class."""

    def __init__(self):
        self.tasks = dict()
        self.output = dict()

    def submit(self, task: Task, *args, **kwargs):
        """
        Submit a job to process pool executor
        :param task: object Task instance to be executed
        :param args:
        :param kwargs:
        """
        self.tasks[task.name] = {
            'task': task,
            'args': args,
            'kwargs': kwargs
        }

    def run(self):
        """"Run pending tasks."""
        for elm in self.tasks:
            self.output[elm] = self.tasks[elm]['task'].run(*self.tasks[elm]['args'], **self.tasks[elm]['kwargs'])

        return self.output
