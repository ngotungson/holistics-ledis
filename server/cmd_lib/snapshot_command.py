import os
from datetime import datetime
import glob, pickle

from storage import *

class SnapshotCommand(object):
    def __init__(self, ins, params=[]):
        self.ins = ins
        self.params = params

    def run(self):
        if self.ins == "SAVE":
            return self._save()
        elif self.ins == "RESTORE":
            return self._restore()

    def _save(self):
        new_snapshot = "snapshots/" + str(datetime.now()) + ".backup"
        with open(new_snapshot, "wb") as f:
            pickle.dump(storage, f, pickle.HIGHEST_PROTOCOL)

    def _restore(self):
        last_snapshot = max(glob.glob('snapshots/*.backup'), key=os.path.getctime)
        with open(last_snapshot, "rb") as f:
            storage.clear()
            storage.update(pickle.load(f))
