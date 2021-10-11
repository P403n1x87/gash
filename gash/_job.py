import typing as t

from gash._step import Step


class Job:
    def __init__(self, workflow, name, data):
        self.workflow = workflow
        self.name = name
        self.data = data

    @property
    def steps(self):
        ss = self.data.get("steps")
        if ss is None:
            return []

        return [Step(self, _) for _ in ss]

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

        for s in self.steps:
            if s.runnable:
                s.run(interactive=interactive)
            else:
                print(f"Skipping unrunnable {s}")

    def __repr__(self):
        return f"Job(name: '{self.name}', workflow: {self.workflow})"

    __str__ = __repr__
