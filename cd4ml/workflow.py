import graphlib

from concurrent.futures import Future

from cd4ml.task import Task


class Workflow(graphlib.TopologicalSorter):
    """Basic workflow class"""

    def __init__(self, *args, **kwargs):
        self.tasks = dict()
        self.valid_executors = [
            'local'
        ]
        self.running_task = None
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

    def get_executor(self, executor):
        if executor not in self.valid_executors:
            raise ValueError(f"Invalid executor {executor}. Available executors: {self.valid_executors}")

        if executor == 'local':
            from cd4ml.executor import LocalExecutor
            return LocalExecutor()

    def run(self, params: dict, executor='local'):
        """
        Run workflow tasks.
        :param params: dict Tasks input and output format. Ex.:
        {
            'add':  (1, 2),
            'add2': (a=1, b=2)
        }
        :param executor:    Type of job executor. Defaults to local asyncio
        :return: dict Output JSON with run results
        {
            'add': 3,
            'add2': 3
        }
        """
        self.prepare()
        exe = self.get_executor(executor=executor)
        # Run all nodes
        while self.is_active():
            # Run any tasks when they are ready
            for task in self.get_ready():
                exe.submit(self.tasks[task], *params[task])

            # Run tasks
            exe.run()

            for elm in exe.output:
                try:
                    self.done(elm)
                except ValueError as e:
                    # This node was alread marked as done
                    print(e)
                    pass

        return exe.output
