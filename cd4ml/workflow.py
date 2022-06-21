import graphlib

from cd4ml.task import Task


class Workflow(graphlib.TopologicalSorter):
    """Basic workflow class"""

    def __init__(self, *args, **kwargs):
        self.tasks = dict()
        super().__init__(*args, **kwargs)

    def add_task(self, func):
        assert isinstance(func, Task)
        self.tasks[func.name] = func

    def run_task(self, name, *args, **kwargs):
        """
        Run task in Workflow

        :param name: str    Task name
        :param args:
        :param kwargs:
        :return: object Task output
        """
        return self.tasks[name].run(*args, **kwargs)

    def run(self, params: dict):
        """
        Run workflow tasks.
        :param params: dict Tasks input and output format. Ex.:
        {
            'add':  (1, 2),
            'add2': (a=1, b=2)
        }
        :return: dict Output JSON with run results
        {
            'add': 3,
            'add2': 3
        }
        """
        pass
