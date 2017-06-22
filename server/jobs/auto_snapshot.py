from storage import *
from cmd_lib import SnapshotCommand

def auto_snapshot():
    SnapshotCommand("SAVE").run()
