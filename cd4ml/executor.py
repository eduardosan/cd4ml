from concurrent.futures import ThreadPoolExecutor, as_completed


class LocalExecutor:
    """Local executor class."""

    def __init__(self, max_workers=2):
        self.pool = ThreadPoolExecutor(max_workers=max_workers)
        self.futures = []

    def submit(self, func, callback, *args, **kwargs):
        """
        Submit a job to process pool executor
        :param func: str Job name
        :param callback: callable   Callback to execute when process is finished
        :param func: callable function to be run on process pool executor
        :param args:
        :param kwargs:
        """
        future = self.pool.submit(func, *args, **kwargs)
        future.add_done_callback(callback)
        self.futures.append(future)
