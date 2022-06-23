from unittest import TestCase
import graphlib

from cd4ml.workflow import Workflow
from cd4ml.task import Task


class TestWorkflow(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_workflow(self):
        """Should start a Workflow"""
        w = Workflow()
        self.assertIsInstance(w, Workflow)
        self.assertIsInstance(w, graphlib.TopologicalSorter)

    def test_add_task(self):
        """Should add a new task to the Workflow."""
        def add(a, b):
            return a + b

        w = Workflow()
        t = Task(name='add', task=add)
        w.add_task(t)
        self.assertIsInstance(w.tasks['add'], Task)

    def test_add_task_run(self):
        """Should add a task run with params for execution."""
        def add(a, b):
            return a + b

        w = Workflow()
        t = Task(name='add', task=add)
        w.add_task(t)
        result = w.run_task('add', 1, 2)
        self.assertEqual(result, 3)

    def test_add_dependency(self):
        """Should add a new node dependency to the Workflow."""
        def add(a, b):
            return a + b

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
        def add(a, b):
            return a + b

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
        def add(a, b):
            return a + b

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
        def add(a, b):
            return a + b

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
        def add(a, b):
            return a + b

        w = Workflow()
        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        w.add_task(t)
        w.add_task(t2, dependency='add')
        output = w.run(params={
            'add': (1, 2),
            'add2': {'a': 2, 'b': 3}
        }, executor='local')

        self.assertDictEqual({'add': 3, 'add2': 5}, output)

    def test_run_format(self):
        """Should run a when parameters are passed as string."""
        def fetch_feed_data(url):
            pass

        download_g1 = Task(name='download_g1', task=fetch_feed_data)
        download_g1_brasil = Task(name='download_g1_brasil', task=fetch_feed_data)
        download_folha = Task(name='download_folha', task=fetch_feed_data)

        feeds_json = {
            "download_folha": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml",
            "download_g1": "https://g1.globo.com/rss/g1/",
            "download_g1_brasil": "https://g1.globo.com/rss/g1/brasil",
        }

        w = Workflow()
        w.add_task(download_g1)
        w.add_task(download_g1_brasil)
        w.add_task(download_folha)
        output = w.run(params=feeds_json, executor='local')
        self.assertDictEqual(output, {'download_folha': None, 'download_g1': None, 'download_g1_brasil': None})
