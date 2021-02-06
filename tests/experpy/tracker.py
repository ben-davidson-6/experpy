import os
import logging

from git import Repo
from experpy.tracker import TrackingRepo

logging.basicConfig(level=logging.FATAL)
logger = logging.getLogger()


def test_tracking_repo_clean(empty_repo: Repo, add_file_to_repo, display_repo_state):
    # make my changes
    f = add_file_to_repo(empty_repo)

    # I remember to add everything
    empty_repo.index.add([f])
    empty_repo.index.commit('I remembered to add it!')

    # check the repo is clean
    tracking_repo = TrackingRepo(empty_repo.working_dir)
    assert not tracking_repo._is_branch_dirty()

    # show the state of the repo
    display_repo_state(empty_repo)


def test_dirty_with_untracked(empty_repo: Repo, add_file_to_repo, display_repo_state):
    # make my changes
    f = add_file_to_repo(empty_repo)

    # i stage but dont commit
    empty_repo.index.add([f])

    # check the repo is dirty
    tracking_repo = TrackingRepo(empty_repo.working_dir)
    assert tracking_repo._is_branch_dirty()

    # show the state of the repo
    display_repo_state(empty_repo)


def test_dirty_with_tracked_not_commited(empty_repo: Repo, add_file_to_repo, display_repo_state):
    # make my changes
    f = add_file_to_repo(empty_repo)

    # check the repo is clean
    tracking_repo = TrackingRepo(empty_repo.working_dir)
    assert tracking_repo._is_branch_dirty()

    # show the state of the repo
    display_repo_state(empty_repo)


def test_make_clean_from_untracked(empty_repo: Repo, add_file_to_repo, display_repo_state):
    # make my changes
    f = add_file_to_repo(empty_repo)

    # make the repo clean
    tracking_repo = TrackingRepo(empty_repo.working_dir)
    assert tracking_repo._is_branch_dirty()
    tracking_repo.ensure_clean_branch()
    assert not tracking_repo._is_branch_dirty()

    # show the state of the repo
    display_repo_state(empty_repo)


def test_make_clean_from_tracked(empty_repo: Repo, add_file_to_repo, display_repo_state):
    # make my changes
    f = add_file_to_repo(empty_repo)

    # i stage but dont commit
    empty_repo.index.add([f])

    # make the repo clean
    tracking_repo = TrackingRepo(empty_repo.working_dir)

    assert tracking_repo._is_branch_dirty()
    tracking_repo.ensure_clean_branch()
    assert not tracking_repo._is_branch_dirty()

    # show the state of the repo
    display_repo_state(empty_repo)


def test_dirty_after_modified(empty_repo: Repo, add_file_to_repo, modify_file, display_repo_state):
    # make my changes
    f = add_file_to_repo(empty_repo)

    # i stage but dont commit
    empty_repo.index.add([f])
    empty_repo.index.commit('im a responsible developer who commits there code')

    # make the repo clean
    tracking_repo = TrackingRepo(empty_repo.working_dir)
    assert not tracking_repo._is_branch_dirty()

    modify_file(f)

    assert tracking_repo._is_branch_dirty()

    # show the state of the repo
    display_repo_state(empty_repo)


def test_clean_from_modified(empty_repo: Repo, add_file_to_repo, modify_file, display_repo_state):
    # make my changes
    f = add_file_to_repo(empty_repo)

    # i stage but dont commit
    empty_repo.index.add([f])
    empty_repo.index.commit('im a responsible developer who commits there code')

    # make the repo clean
    tracking_repo = TrackingRepo(empty_repo.working_dir)
    assert not tracking_repo._is_branch_dirty()

    modify_file(f)

    assert tracking_repo._is_branch_dirty()
    tracking_repo.ensure_clean_branch()

    assert not tracking_repo._is_branch_dirty()

    # show the state of the repo
    display_repo_state(empty_repo)


def test_doesnt_add_ignored_from_existing(empty_repo: Repo, add_file_to_repo, modify_file, display_repo_state):
    # add some file that I should ignore
    f = add_file_to_repo(empty_repo)
    name = os.path.basename(f)
    gitignore = name
    with open(os.path.join(empty_repo.working_dir, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # i stage but dont commit
    empty_repo.index.add(['.gitignore'])

    empty_repo.index.commit('added ignore')

    # make the repo clean
    tracking_repo = TrackingRepo(empty_repo.working_dir)
    assert not tracking_repo._is_branch_dirty()

    # show the state of the repo
    display_repo_state(empty_repo)


def test_doesnt_add_ignored_in_same(empty_repo: Repo, add_file_to_repo, modify_file, display_repo_state):
    # add some file that I should ignore
    f = add_file_to_repo(empty_repo)
    name = os.path.basename(f)
    gitignore = name
    with open(os.path.join(empty_repo.working_dir, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # make the repo clean
    tracking_repo = TrackingRepo(empty_repo.working_dir)
    tracking_repo.ensure_clean_branch()

    assert len(tracking_repo.head.commit.stats.files.keys()) == 1

    # show the state of the repo
    display_repo_state(empty_repo)
