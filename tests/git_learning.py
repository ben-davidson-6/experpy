import logging
from git import Repo

logging.basicConfig(level=logging.FATAL)
logger = logging.getLogger()

def test_make_add_tag(empty_repo: Repo, add_file_to_repo, display_repo_state):

    # we make some alg
    f = add_file_to_repo(empty_repo)

    # we commit
    empty_repo.index.add([f])
    empty_repo.index.commit('added amazing network')

    # we start training and finish with a good metric
    metric = 0.99
    empty_repo.create_tag(f'experpy-{metric}')

    display_repo_state(empty_repo)


def test_find_untracked_or_modified(empty_repo: Repo, add_file_to_repo, modify_file, display_repo_state):

    # we make some killer algorithm
    f = add_file_to_repo(empty_repo)

    # but woops we forget to commit or whatever
    not_tracked = empty_repo.untracked_files
    logger.info(f'files not tracked: {not_tracked}')
    assert len(not_tracked) == 1
    empty_repo.index.add([f])
    assert len(empty_repo.untracked_files) == 0

    # but the changes are not commited
    diff_from_head = empty_repo.head.commit.diff(None)
    logger.info(f'diffs: {diff_from_head}')
    assert len(diff_from_head) == 1
    empty_repo.index.commit('AUTO COMMIT epxerpy')

    diff_from_head = empty_repo.head.commit.diff(None)
    assert len(diff_from_head) == 0

    # we update the algoirthm
    modify_file(f)
    diff_from_head = empty_repo.head.commit.diff(None)
    assert len(diff_from_head) == 1

    # we start training and finish with a good metric
    metric = 0.99
    empty_repo.create_tag(f'experpy-{metric}')

    display_repo_state(empty_repo)
