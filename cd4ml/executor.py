from cd4ml.task import Task


class LocalExecutor:
    """Local executor class."""

    def __init__(self, experiment_id='latest'):
        self.tasks = dict()
        self.output = dict()
        self.done = list()
        self.experiment_id = experiment_id

    def submit(self, task: Task, params: dict = None, output=None):
        """
        Submit a job to process pool executor.

        :param Task task: Task instance to be executed
        :param dict params: parameters dict for the task
        :param str output: Name of output var
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
