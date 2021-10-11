import typing as t
from pathlib import Path

from gash._job import Job
from gash._workflow import Workflow


def get_workflows_path() -> Path:
    dirs = list(Path.cwd().parents)
    dirs.insert(0, Path.cwd())
    for d in dirs:
        path = d.joinpath(".github", "workflows")
        if path.is_dir():
            return path
    else:
        raise RuntimeError("No workflows in currenty directory")


def workflows() -> t.Generator[Workflow, None, None]:
    wfpath = get_workflows_path()

    yield from (
        Workflow(_)
        for _ in [wfpath.joinpath(_) for _ in wfpath.iterdir() if _.suffix == ".yaml"]
        if _.is_file()
    )


def get_workflow(name: str) -> t.Optional[Workflow]:
    for w in workflows():
        if w.name == name:
            return w

    return None


def get_job(wf_name: str, job_name: str) -> t.Optional[Job]:
    w = get_workflow(wf_name)
    if w is not None:
        for j in w.jobs:
            if j.name == job_name:
                return j
    return None


def get_step(wf_name: str, job_name: str, step_name: str):
    j = get_job(wf_name, job_name)
    if j is not None:
        for s in j.steps:
            if s.name == step_name:
                return s
    return None
