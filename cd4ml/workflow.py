import graphlib

from cd4ml.task import Task


class Workflow(graphlib.TopologicalSorter):
    """Basic workflow class"""

    def __init__(self, *args, **kwargs):
        self.tasks = dict()
        super().__init__(*args, **kwargs)

    @property
    def tasks_order(self):
        return [*self.static_order()]

    def add_task(self, func, dependency=None):
        """
        Add a new task to the workflow
        :param func: Function to be executed
        :param dependency: Task dependency name
        :return:
        """
        assert isinstance(func, Task)
        self.tasks[func.name] = func
        if dependency is not None:
            assert dependency in self.tasks
            self.add(func.name, dependency)
        else:
            self.add(func.name)

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
