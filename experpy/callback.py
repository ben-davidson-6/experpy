import tensorflow as tf

from experpy.tracker import Tracker


class GitTracker(tf.keras.callbacks.Callback):
    def __init__(self, tracker: Tracker):
        super(GitTracker, self).__init__()
        self.tracker = tracker
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

    