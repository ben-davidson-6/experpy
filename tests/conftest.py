import pytest
import tempfile
import logging

from git import Repo

logging.basicConfig(level=logging.INFO)
test_logger = logging.getLogger()


@pytest.fixture
def empty_repo():
    with tempfile.TemporaryDirectory() as temp:
        repo = Repo.init(temp)
        repo.index.commit('initial')
        yield repo


@pytest.fixture
def display_repo_state():
    def _display_repo_state(repo):
        info = repo.git.log('--oneline', '--decorate', '--graph', '--all')
        test_logger.info(info)
    return _display_repo_state


@pytest.fixture
def add_file_to_repo():

    def adder(repo: Repo):
        folder = repo.working_dir
        temp_name = tempfile.mktemp(dir=folder,)
        with open(temp_name, 'wb') as f:
            f.write(b'1')
        return temp_name

    return adder


@pytest.fixture
def modify_file():

    def modder(fpath):
        with open(fpath, 'ab') as f:
            f.write(b'2')

    return modder

