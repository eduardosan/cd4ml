import unittest

from concurrent.futures import as_completed

from cd4ml.executor import LocalExecutor


class TestExecutor(unittest.TestCase):
    """Test local executor."""
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create_pool(self):
        """Should create a process pool"""
        e = LocalExecutor()
        self.assertIsInstance(e, LocalExecutor)

    def test_pool_submit(self):
        """Should submit a job to process pool."""
        def add(a, b):
            return a + b

        e = LocalExecutor()
        e.submit(add, lambda x: print("Oi"), 1, 2)
        self.assertEqual(len(e.futures), 1)

    def test_completed(self):
        """Should return result when a job is completed"""
        def add(a, b):
            return a + b

        def add_callback(future):
            print(f"Result: {future.result()}")

        e = LocalExecutor()
        e.submit(add, add_callback, 1, 2)
        for x in as_completed(e.futures):
            self.assertEqual(x.result(), 3)

    def test_pool_submit_jobs(self):
        """Should submit multiple jobs to process pool"""

        def add(a, b):
            return a + b

        def add_callback(future):
            print(f"Result: {future.result()}")

        e = LocalExecutor()
        e.submit(add, add_callback, 1, 2)
        e.submit(add, add_callback, 1, 2)
        e.submit(add, add_callback, 1, 2)
        e.submit(add, add_callback, 1, 2)
        for x in as_completed(e.futures):
            self.assertEqual(x.result(), 3)
