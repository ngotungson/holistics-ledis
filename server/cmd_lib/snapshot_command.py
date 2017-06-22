import os
from datetime import datetime
import glob, pickle

from storage import *
from base_command import BaseCommand

class SnapshotCommand(BaseCommand):
    def __init__(self, ins, params=[]):
        BaseCommand.__init__(self, ins, params)

    def run(self):
        if self.ins == "SAVE":
            return self._save()

        elif self.ins == "RESTORE":
            return self._restore()


    def _save(self):
        new_snapshot = "snapshots/" + str(datetime.now()) + ".backup"
        with open(new_snapshot, "wb") as f:
            pickle.dump(storage, f, pickle.HIGHEST_PROTOCOL)
        return "Saved"

    def _restore(self):
        last_snapshot = max(glob.glob('snapshots/*.backup'), key=os.path.getctime)
        with open(last_snapshot, "rb") as f:
            storage.clear()
            storage.update(pickle.load(f))
        return "Restored"
