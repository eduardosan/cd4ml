from cd4ml.task import Task


class LocalExecutor:
    """Local executor class."""

    def __init__(self):
        self.tasks = dict()
        self.output = dict()
        self.done = list()

    def submit(self, task: Task, params: dict = None, output=None):
        """
        Submit a job to process pool executor
        :param task: object Task instance to be executed
        :param params: parameters dict for the task
        :param output: str  Name of output var
        """
        if not isinstance(params, dict) and params is not None:
            raise TypeError(f"We only accept dict as params you supplied '{type(params)}' for {params}")

        self.tasks[task.name] = {
            'task': task,
            'params': params,
            'output': output
        }

    def run(self):
        """"Run pending tasks."""
        for elm in self.tasks:
            try:
                result = self.tasks[elm]['task'].run(**self.tasks[elm]['params'])
            except TypeError:
                # Try again with no params
                result = self.tasks[elm]['task'].run()

            if self.tasks[elm]['output'] is not None:
                self.output[self.tasks[elm]['output']] = result

            # Add task to done list
            self.done.append(elm)

        return self.output
