import tensorflow as tf
import inspect
import git

from experpy.tracker import Tracker, TrackingRepo, TrackingMetric
from pathlib import Path


class GitTrackCallback(tf.keras.callbacks.Callback):
    def __init__(self, metric_name: str, mode: str):
        super(GitTrackCallback, self).__init__()

        # build the tracker
        caller_location = GitTrackCallback._get_caller_location()
        repo_location = GitTrackCallback._find_caller_git_repo(caller_location)
        repo = TrackingRepo(repo_location)
        metric = TrackingMetric(metric_name, mode)

        self.tracker = Tracker(repo, metric)
        self.first_epoch = True

    def on_epoch_end(self, epoch, logs):
        self._is_well_defined(logs)
        self.track(logs)
    
    def track(self, logs):
        name = self.tracker.metric_name()
        value = logs[name]
        self.tracker.update_metric(value)
        self.tracker.track()

    def _is_well_defined(self, logs):
        if self.first_epoch:
            # check that the metric we want exists
            metric_is_in_logs = self.tracker.metric_name() in logs
            error_msg = f'Metric {self.tracker.metric_name()} not found in log keys:\n{list(logs.keys())}'
            assert metric_is_in_logs, error_msg

            # clean the branch so we can commit when we need to
            self.tracker.clean_branch()
        self.first_epoch = False
        return True

    @staticmethod
    def _get_caller_location():
        # we need to jump back twice since we call this from the constructor
        previous_frame = inspect.currentframe().f_back.f_back
        filename, *_ = inspect.getframeinfo(previous_frame)
        return Path(filename).parent

    @staticmethod
    def _find_caller_git_repo(caller_location):
        num_parents = len(caller_location.parents)
        current_dir = caller_location
        for _ in range(num_parents):
            if is_git_repo(current_dir):
                return current_dir
            else:
                current_dir = current_dir.parent
        raise git.exc.InvalidGitRepositoryError(f'could not find a git repo from caller {caller_location}')


def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False
