import copy
import graphlib

from cd4ml.task import Task
from cd4ml.utils import graph_to_dot, draw_graph
from cd4ml.experiment import Experiment
from cd4ml.log import logger

tmpgraph = None


class Workflow(graphlib.TopologicalSorter):
    """Basic workflow class"""

    def __init__(self, experiment: Experiment = None, *args, **kwargs):
        self.tasks = dict()
        self.valid_executors = [
            'local'
        ]
        self.running_task = None
        self.experiment = experiment
        super().__init__(*args, **kwargs)

    @property
    def tasks_order(self):
        return [*self.static_order()]

    def add_task(self, func, dependency=None):
        """
        Add a new task to the workflow.

        :param Task func: Function to be executed
        :param str, List[str] dependency: Task dependency names
        """
        assert isinstance(func, Task)
        self.tasks[func.name] = {
            'task': func,
            'dependency': dependency
        }
        if dependency is not None:
            if isinstance(dependency, list):
                for elm in dependency:
                    assert elm in self.tasks
                    self.add(func.name, elm)
            else:
                assert dependency in self.tasks
                self.add(func.name, dependency)
        else:
            self.add(func.name)

    def run_task(self, name, *args, **kwargs):
        """
        Run task in Workflow

        :param str name: Task name
        :param args:
        :param kwargs:
        :return dict: Task output
        """
        return self.tasks[name]['task'].run(*args, **kwargs)

    def get_executor(self, executor):
        if executor not in self.valid_executors:
            raise ValueError(f"Invalid executor {executor}. Available executors: {self.valid_executors}")

        if executor == 'local':
            from cd4ml.executor import LocalExecutor
            return LocalExecutor(experiment=self.experiment)

    def run(self, run_config: dict, executor='local'):
        """
        Run workflow tasks.

        :param dict run_config: Tasks input and output format.
        :param str executor: Type of job executor. Can be one of the following:

            * ``'local'``: runs in local executor
        :return: Output JSON with run results
        :rtype: dict
        :example:

        >>> def add(a, b):
        >>>    return a + b
        >>> w = Workflow()
        >>> t = Task(name='add', task=add)
        >>> t2 = Task(name='add2', task=add)
        >>> w.run(run_config={
        >>>    'add': {
        >>>        'params': {'a': 1, 'b': 2},
        >>>        'output': 'add'
        >>>    },
        >>>    'add2': {
        >>>        'params': {'a': 2, 'b': 3},
        >>>        'output': 'add2'
        >>>    }
        >>> }, executor='local')
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
                if self.tasks[task].get('dependency') is not None:
                    run_config[task]['params'] = dict()

                    if isinstance(self.tasks[task]['dependency'], list):
                        for elm in self.tasks[task]['dependency']:
                            # Get output name from task workflow configuration
                            output_var = run_config[elm]['output']

                            # Get parameters from experiment provider, if it exists
                            if self.experiment is not None:
                                # TODO: support pandas as input
                                run_config[task]['params'][output_var] = self.experiment.load_output(
                                    name=output_var)
                            else:
                                run_config[task]['params'][output_var] = exe.output[output_var]
                    else:
                        output_var = run_config[self.tasks[task]['dependency']]['output']
                        if self.experiment is not None:
                            run_config[task]['params'][output_var] = self.experiment.load_output(name=output_var)
                        else:
                            run_config[task]['params'][output_var] = exe.output[output_var]

                logger.info(f"Submitting task {task} to executor {executor}")
                exe.submit(self.tasks[task]['task'], params=run_config[task]['params'],
                           output=run_config[task].get('output'))

            # Run tasks
            logger.info("Running workflow...")
            exe.run()

            for elm in exe.done:
                logger.info(f"Marking task {elm} as done...")
                try:
                    self.done(elm)
                except ValueError as e:
                    # This node was already marked as done
                    print(e)
                    pass

        return exe.output

    def dotfile(self, filepath: str):
        """
        Generate a dotfile from graph.

        :param str filepath: Filepath to save the dotfile
        :return str: Filepath with the file saved
        """
        dotstring = graph_to_dot(self)

        # Generate dotfile in tmp dir
        with open(filepath, 'w+') as fd:
            fd.write(dotstring)

        return filepath

    def draw(self, filepath: str = None):
        """
        Draw graph to the output.

        :param str filepath: Filepath to save the drawing output
        :return: Graph instance to print on output
        :rtype: `pygraphviz.Agraph <https://pygraphviz.github.io/documentation/stable/reference/agraph.html>`_
        """
        return draw_graph(self, filepath=filepath)

    def prepare(self) -> None:
        """Just copy object before it starts processing the graph, so we can run it multiple times"""
        global tmpgraph
        tmpgraph = graphlib.TopologicalSorter()
        tmpgraph._node2info = copy.deepcopy(self._node2info)
        tmpgraph._ready_nodes = copy.deepcopy(self._ready_nodes)
        super().prepare()

    def reset(self):
        """Restore previous objects so we can run the workflow again"""
        self._ready_nodes = tmpgraph._ready_nodes
        self._node2info = tmpgraph._node2info
