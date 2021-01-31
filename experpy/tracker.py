from git import Repo
from git.refs.head import Head

from experpy.constants import TAG_PREFIX, AUTOCOMMIT_MESSAGE


class Metric:
    def __init__(self, label: str):
        self.label = label

    def build_tag(self, value):
        return f'{TAG_PREFIX}-{self.label}-{value}'


class TrackingRepo(Repo):
    def ensure_clean_branch(self,):
        if self._is_branch_dirty():
            self._track_untracked()
            self._stage_modified()
            self._commit_changes()

    def _is_branch_dirty(self):
        no_untracked = len(self.untracked_files) > 0
        no_diffs = len(self._all_difs()) > 0
        return no_diffs or no_untracked

    def _all_difs(self):
        return self.head.commit.diff(None)

    def _track_untracked(self):
        if self.untracked_files:
            self.index.add(self.untracked_files)

    def _stage_modified(self):
        self.index.add([x.a_path for x in self._all_difs()])

    def _commit_changes(self, ):
        self.index.commit(AUTOCOMMIT_MESSAGE)


class Tracker:
    def __init__(self, repo: TrackingRepo, metric: Metric):
        self.repo = repo
        self.metric = metric

    def track(self, value):
        self.repo.ensure_clean_branch()
        self.tag_latest_commit(value)

    def tag_latest_commit(self, value):
        tag = self.metric.build_tag(value)
        self.repo.create_tag(tag)
