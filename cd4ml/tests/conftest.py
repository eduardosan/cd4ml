import pytest
import os.path
import shutil


@pytest.fixture(scope='session')
def test_dir(request):
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope='session')
def dotfile(request, test_dir):
    """
    Get dotfile from test dir

    :param request:
    :param test_dir: testing directory
    """
    return os.path.join(test_dir, "./fixtures/complex.dot")


@pytest.fixture(scope='class')
def get_dotfile(request, dotfile):
    request.cls.dotfile = dotfile


@pytest.fixture(scope='class')
def get_dotfile_path(request, tmp_path_factory):
    request.cls.dotfile_path = tmp_path_factory.mktemp("data") / "complex.dot"


@pytest.fixture(scope='session')
def experiment_repository(request, tmp_path_factory):
    return tmp_path_factory.mktemp("data") / ".cd4ml"


@pytest.fixture(scope='class')
def get_local_experiment_repository(request, experiment_repository):
    request.cls.local_experiment_repository = experiment_repository
