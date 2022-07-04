import unittest

from cd4ml.contracts.artifact import Artifact,ArtifactsHandler


class DummyArtifactHandler(ArtifactsHandler):

    def save(self,artifacts:list[Artifact],path:str):
        artifacts
        path

    def load(self,parameters: dict, path: str) -> list[Artifact]:
        return [Artifact(name='test',object=None,params={'params':'params'})]    

class TestArtifactHandler(unittest.TestCase):
    """Test artifact handler to save and load artifacts."""
    
    def setUp(self) -> None:
        self.artifact_handler = DummyArtifactHandler()

    def tearDown(self) -> None:
        pass
    
    def test_artifact_handler_instance(self):
        # self.artifact_handler: ArtifactsHandler = DummyArtifactHandler()
        self.assertIsInstance(self.artifact_handler,ArtifactsHandler)

    def test_save(self):
        """Should accept a list of artifacts and save them."""
        # self.artifact_handler : ArtifactsHandler = DummyArtifactHandler()
        artifacts = [Artifact(name='test',object=None,params={'params':'params'})] 
        self.assertTrue(self.artifact_handler.save(artifacts=artifacts,path=''))

    def test_save(self):
        """Should return a list of Artifacts based on a parameters dict and path string."""
        # self.artifact_handler:ArtifactsHandler = DummyArtifactHandler()

        artifacts_reference = [Artifact(name='test',object=None,params={'params':'params'})] 
        self.assertTrue(self.artifact_handler.load(artifacts=artifacts,path=''))

        artifacts = self.artifact_handler.load(parameters={},path='')
        self.assertEqual(artifacts_reference,artifacts)