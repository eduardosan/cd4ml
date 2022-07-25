from cd4ml.task import Task
from cd4ml.experiment import Experiment as Exp
from cd4ml.log import logger


class LocalExecutor:
    """Local executor class."""

    def __init__(self, experiment: Exp = None):
        self.tasks = dict()
        self.output = dict()
        self.done = list()
        self.experiment = experiment

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

                # Save output on experiments repository
                if self.experiment is not None:
                    logger.info(f"Saving task {elm} output on path {self.experiment.provider.repository_path}")
                    self.experiment.save_output(name=self.tasks[elm]['output'], data=result)

            # Add task to done list
            self.done.append(elm)

        return self.output
