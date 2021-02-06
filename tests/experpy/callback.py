from experpy.callback import GitTrackCallback
from pathlib import Path

def test():
    pass

def test_gets_right_location():
    # test is a little sketch as we are reading our own code repo
    callback = GitTrackCallback('val_loss', 'max')
    assert callback.tracker.repo.working_dir == str(Path(__file__).parent.parent.parent.resolve())
