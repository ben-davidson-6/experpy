from git import Repo
from experpy.constants import AUTOCOMMIT_MESSAGE, TAG_PREFIX, MIN, MAX


class TrackingMetric:

    def __init__(self, name: str, mode: str):
        self.name = name
        self.mode = mode.upper()
        self.value = None
        assert self.mode in [MAX, MIN]

    def update(self, value):
        if self.is_value_better(value):
            self.value = value

    def is_value_better(self, value):
        if self.value is None:
            is_better = True
        elif self.mode == MIN:
            is_better = value < self.value
        elif self.mode == MAX:
            is_better = value > self.value
        else:
            raise ValueError('unreachable!?!?!')
        return is_better

    def build_tag(self,):
        if self.value is None:
            raise ValueError(f'The metric {self.name} has not recieved a value')
        return f'{TAG_PREFIX}-{self.name}-{self.value}'

    def get_name(self):
        return self.name


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
    def __init__(self, repo: TrackingRepo, metric: TrackingMetric):
        self.repo = repo
        self.metric = metric
        self.last_tag_ref = None

    def clean_branch(self):
        self.repo.ensure_clean_branch()

    def track(self,):
        self.clean_branch()
        self._tag_latest_commit()

    def _tag_latest_commit(self,):
        self._delete_last_tag()
        tag = self.metric.build_tag()
        self.last_tag_ref = self.repo.create_tag(tag)

    def update_metric(self, value):
        self.metric.update(value)

    def metric_name(self):
        return self.metric.get_name()
    
    def _delete_last_tag(self,):
        if self.last_tag_ref is None:
            pass
        else:
            self.repo.delete_tag(self.last_tag_ref)
            self.last_tag_ref = None
