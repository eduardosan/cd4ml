import pytest
import os.path


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
