from subprocess import PIPE, check_output


class Step:
    def __init__(self, job, data):
        self.job = job
        self.data = data

    @property
    def runnable(self):
        return "uses" not in self.data and "run" in self.data

    def run(self, interactive=False):
        if not self.runnable:
            raise RuntimeError(f"{self} is not runnable")

        if interactive:
            while True:
                _ = input(f"About to run {self}. Continue? [Y/n] ")
                if _.lower() in {"n", "no"}:
                    return
                if _.lower() not in {"y", "yes", ""}:
                    print("Invalid answer.")
                    continue
                break

        print(f"Running {self}...")
        for line in self.data["run"].splitlines():
            print(f"> {line}")

        print(check_output(self.data["run"], stderr=PIPE, shell=True).decode())

    @property
    def name(self):
        return self.data.get("name")

    def __repr__(self):
        name = self.name
        name = f"'{name}'" if name is not None else "anonymous"
        uses = self.data.get("uses")
        uses_string = f", uses: {uses}" if uses is not None else ""
        return f"Step(name: {name}, runnable: {self.runnable}{uses_string}, job: {self.job})"

    __str__ = __repr__
