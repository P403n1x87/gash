import typing as t

import yaml

from gash._job import Job


class Workflow:
    @staticmethod
    def _load(path):
        with open(path) as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    def __init__(self, path):
        self.path = path
        self._data = self._load(path)

    @property
    def name(self):
        return self._data["name"]

    @property
    def jobs(self):
        js = self._data.get("jobs")
        if js is None:
            return []

        return [Job(self, n, d) for n, d in js.items()]

    def run(self, interactive=False):
        if interactive:
            while True:
                _ = input(f"About to run {self}. Continue? [Y/n] ")
                if _.lower() in {"n", "no"}:
                    return
                if _.lower() not in {"y", "yes", ""}:
                    print("Invalid answer.")
                    continue
                break

        for j in self.jobs:
            j.run(interactive=interactive)

    def __repr__(self):
        return f"Workflow(name: '{self.name}', path: {self.path})"

    __str__ = __repr__
