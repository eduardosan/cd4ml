import graphlib


class Workflow(graphlib.TopologicalSorter):
    """Basic workflow class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
