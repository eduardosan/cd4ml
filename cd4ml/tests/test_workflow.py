import io
import graphlib
import pytest
from unittest import TestCase

from cd4ml.workflow import Workflow
from cd4ml.task import Task
from cd4ml.experiment import LocalExperimentProvider, Experiment


def add(a, b):
    return a + b


@pytest.mark.usefixtures('get_local_experiment_repository')
class TestWorkflow(TestCase):
    def setUp(self) -> None:
        provider = LocalExperimentProvider(repository_path=self.local_experiment_repository)
        self.experiment = Experiment(provider=provider)

    def tearDown(self) -> None:
        pass

    def test_workflow(self):
        """Should start a Workflow"""
        w = Workflow()
        self.assertIsInstance(w, Workflow)
        self.assertIsInstance(w, graphlib.TopologicalSorter)

    def test_add_task(self):
        """Should add a new task to the Workflow."""
        w = Workflow()
        t = Task(name='add', task=add)
        w.add_task(t)
        self.assertIsInstance(w.tasks['add']['task'], Task)

    def test_add_task_run(self):
        """Should add a task run with params for execution."""
        w = Workflow()
        t = Task(name='add', task=add)
        w.add_task(t)
        result = w.run_task('add', 1, 2)
        self.assertEqual(result, 3)

    def test_add_dependency(self):
        """Should add a new node dependency to the Workflow."""
        w = Workflow()
        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        t3 = Task(name='add3', task=add)
        w.add_task(t)
        w.add_task(t2, dependency='add')
        w.add_task(t3, dependency='add2')
        self.assertListEqual(['add', 'add2', 'add3'], w.tasks_order)

    def test_add_complex_dependencies(self):
        """Should map multilevel dependencies in a graph"""
        w = Workflow()
        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        t3 = Task(name='add3', task=add)
        t4 = Task(name='add4', task=add)
        t5 = Task(name='add5', task=add)
        t6 = Task(name='add6', task=add)
        t7 = Task(name='add7', task=add)
        t8 = Task(name='add8', task=add)
        t9 = Task(name='add9', task=add)
        w.add_task(t)
        w.add_task(t2, dependency='add')
        w.add_task(t3, dependency='add')
        w.add_task(t4, dependency='add2')
        w.add_task(t5, dependency='add2')
        w.add_task(t6, dependency='add')
        w.add_task(t7, dependency='add5')
        w.add_task(t8, dependency='add6')
        w.add_task(t9)
        self.assertListEqual(['add', 'add9', 'add2', 'add3', 'add6', 'add4', 'add5', 'add8', 'add7'], w.tasks_order)

    def test_add_multiple_dependencies(self):
        """Should allow multiple dependencies for the same node."""
        w = Workflow()
        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        t3 = Task(name='add3', task=add)
        t4 = Task(name='add4', task=add)
        w.add_task(t)
        w.add_task(t2)
        w.add_task(t4)
        w.add_task(t3, dependency=['add', 'add2', 'add4'])
        self.assertListEqual(['add', 'add2', 'add4', 'add3'], w.tasks_order)

    def test_node_add_done(self):
        """Should mark a task as done."""
        w = Workflow()
        t = Task(name='add', task=add)
        w.add_task(t)
        w.prepare()
        for task in w.get_ready():
            if task == 'add':
                w.done(task)
        self.assertFalse(w.is_active())

    def test_run(self):
        """Run simple workflow with two tasks"""
        w = Workflow()
        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        w.add_task(t)
        w.add_task(t2)
        output = w.run(run_config={
            'add': {
                'params': {'a': 1, 'b': 2},
                'output': 'add'
            },
            'add2': {
                'params': {'a': 2, 'b': 3},
                'output': 'add2'
            }
        }, executor='local')

        self.assertDictEqual({'add': 3, 'add2': 5}, output)

    def test_run_format(self):
        """Should run a when parameters are passed as string."""
        def fetch_feed_data(url):
            pass

        download_g1 = Task(name='download_g1', task=fetch_feed_data)
        download_g1_brasil = Task(name='download_g1_brasil', task=fetch_feed_data)
        download_folha = Task(name='download_folha', task=fetch_feed_data)

        run_config = {
            "download_folha": {
                'params': {'url': "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml"},
                'output': 'download_folha'
            },
            "download_g1": {
                'params': {'url': "https://g1.globo.com/rss/g1/"},
                'output': 'download_g1'
            },
            "download_g1_brasil": {
                'params': {'url': "https://g1.globo.com/rss/g1/brasil"},
                'output': 'download_g1_brasil'
            },
        }

        w = Workflow()
        w.add_task(download_g1)
        w.add_task(download_g1_brasil)
        w.add_task(download_folha)
        output = w.run(run_config=run_config, executor='local')
        self.assertDictEqual(output, {'download_folha': None, 'download_g1': None, 'download_g1_brasil': None})

    def test_run_dependency_with_output(self):
        """Should read dependency params from previous task in the workflow."""
        def increment(c):
            return c + 1

        t = Task(name='add', task=add)
        t2 = Task(name='increment', task=increment)
        w = Workflow()
        w.add_task(t)
        w.add_task(t2, dependency='add')
        output = w.run(run_config={
            'add': {
                'params': {'a': 1, 'b': 2},
                'output': 'c'
            },
            'increment': {
                'params': None,
                'output': 'increment'
            }
        }, executor='local')
        self.assertEqual(output['increment'], 4)

    def test_run_dependency_with_output_raises(self):
        """Should raise an error if dependency doesn't return an output."""
        def increment(c):
            return c + 1

        t = Task(name='add', task=add)
        t2 = Task(name='increment', task=increment)
        w = Workflow()
        w.add_task(t)
        w.add_task(t2, dependency='add')
        with self.assertRaises(KeyError):
            w.run(run_config={
                'add': {'params': {'a': 1, 'b': 2}},
                'increment': {'params': None}
            }, executor='local')

    def test_run_multiple_dependencies_with_output(self):
        """Should read multiple dependency params from previous tasks in the workflow."""
        def increment(c, d):
            return (c + d) + 1
        t = Task(name='add', task=add)
        t2 = Task(name='increment', task=increment)
        t3 = Task(name='add2', task=add)
        w = Workflow()
        w.add_task(t)
        w.add_task(t3)
        w.add_task(t2, dependency=['add', 'add2'])
        output = w.run(run_config={
            'add': {
                'params': {'a': 1, 'b': 2},
                'output': 'c'
            },
            'add2': {
                'params': {'a': 3, 'b': 4},
                'output': 'd'
            },
            'increment': {
                'params': None,
                'output': 'increment'
            }
        }, executor='local')
        self.assertEqual(output['increment'], 11)

    @pytest.mark.usefixtures('get_dotfile', 'get_dotfile_path')
    def test_graph_dot_generate(self):
        """Should generate a dot file for the provided graph."""
        w = Workflow()
        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        t3 = Task(name='add3', task=add)
        t4 = Task(name='add4', task=add)
        t5 = Task(name='add5', task=add)
        t6 = Task(name='add6', task=add)
        t7 = Task(name='add7', task=add)
        t8 = Task(name='add8', task=add)
        t9 = Task(name='add9', task=add)
        w.add_task(t)
        w.add_task(t2, dependency='add')
        w.add_task(t3, dependency='add')
        w.add_task(t4, dependency='add2')
        w.add_task(t5, dependency='add2')
        w.add_task(t6, dependency='add')
        w.add_task(t7, dependency='add5')
        w.add_task(t8, dependency='add6')
        w.add_task(t9)

        dotfile = w.dotfile(self.dotfile_path)
        dot = io.open(dotfile).read()
        dotfile = io.open(self.dotfile).read()
        self.assertListEqual(dot.split(), dotfile.split())

    def test_workflow_reset(self):
        """Should be able to reset the workflow to execute multiple times."""
        w = Workflow()
        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        t3 = Task(name='add3', task=add)
        t4 = Task(name='add4', task=add)
        w.add_task(t)
        w.add_task(t2)
        w.add_task(t4)
        w.add_task(t3, dependency=['add', 'add2', 'add4'])
        order1 = w.tasks_order
        w.reset()
        order2 = w.tasks_order
        self.assertListEqual(order1, order2)

    def test_workflow_save_output(self):
        """Should save workflow dependencies output to experiment"""
        w = Workflow(experiment=self.experiment)
        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        w.add_task(t)
        w.add_task(t2)
        output = w.run(run_config={
            'add': {
                'params': {'a': 1, 'b': 2},
                'output': 'add'
            },
            'add2': {
                'params': {'a': 2, 'b': 3},
                'output': 'add2'
            }
        }, executor='local')
        add_var = self.experiment.load_output(name='add')
        add_var2 = self.experiment.load_output(name='add2')
        self.assertEqual(output['add'], add_var)
        self.assertEqual(output['add2'], add_var2)

    def test_workflow_dependency_load_saved_output(self):
        """Should use a previously saved output on next step of workflow."""
        def increment(c):
            return c + 1

        t = Task(name='add', task=add)
        t2 = Task(name='increment', task=increment)
        w = Workflow(experiment=self.experiment)
        w.add_task(t)
        w.add_task(t2, dependency='add')
        w.run(run_config={
            'add': {
                'params': {'a': 1, 'b': 2},
                'output': 'c'
            },
            'increment': {
                'params': None,
                'output': 'increment'
            }
        }, executor='local')
        increment_var = self.experiment.load_output(name='increment')
        self.assertEqual(increment_var, 4)
