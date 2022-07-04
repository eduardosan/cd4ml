import unittest
from typing import Any

from cd4ml.contracts.data_processor import DataProcessor


class DummyDataProcessor(DataProcessor):

    def load_data(self):
        return 'dummy_data'

    def preprocess(self,raw_data: Any) -> Any:
        return raw_data

class TestArtifactHandler(unittest.TestCase):
    """Test artifact handler to save and load artifacts."""
    
    def setUp(self) -> None:
        self.data_processor:DataProcessor = DummyDataProcessor()

    def tearDown(self) -> None:
        pass
    
    def test_data_processor_instance(self):
        # self.data_processor: DataProcessor = DummyDataProcessor()
        self.assertIsInstance(self.data_processor,DataProcessor)

    def test_load_data(self):
        """Should return an object that represents data loaded into memory."""
        # self.data_processor : DataProcessor = DummyDataProcessor()
        self.assertTrue(self.data_processor.load_data())

    def test_load_data(self):
        """Should return an object that represents preprocessed data."""
        # self.data_processor : DataProcessor = DummyDataProcessor()

        raw_data = 'raw_data'
        self.assertTrue(self.data_processor.preprocess(raw_data=raw_data))

        processed_data = self.data_processor.preprocess(raw_data=raw_data)
        self.assertIsNotNone(processed_data)
