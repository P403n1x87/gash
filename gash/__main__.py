import typing as t

import typer

from gash._model import get_job, get_step, get_workflow, workflows

main = typer.Typer()


@main.command(name="list")
def list_workflows():
    for w in workflows():
        typer.echo(w)


@main.command()
def jobs(name: str):
    w = get_workflow(name)
    if w is not None:
        for j in w.jobs:
            typer.echo(j)
    else:
        raise RuntimeError("No workflow named '%s'", name)


@main.command()
def steps(name: str):
    wf_name, _, job_name = name.partition(".")
    j = get_job(wf_name, job_name)
    if j is not None:
        for s in j.steps:
            typer.echo(s)
    else:
        raise RuntimeError("No workflow named '%s'", name)


@main.command()
def run(
    name: str,
    interactive: bool = typer.Option(False, "-i", "--interactive"),
):
    parts = name.split(".", maxsplit=2)
    if len(parts) == 1:
        # We run all jobs for the given workflow
        w = get_workflow(*parts)
        if w is not None:
            for job in w.jobs:
                job.run(interactive=interactive)
        else:
            raise RuntimeError(f"No such workflow: {name}")

    elif len(parts) == 2:
        # We run the given job only
        j = get_job(*parts)
        if j is not None:
            j.run(interactive=interactive)
        else:
            raise RuntimeError(f"No such job: {name}")

    else:
        # We run the given step of the given job only
        s = get_step(*parts)
        if s is not None:
            s.run(interactive=interactive)
        else:
            raise RuntimeError(f"No such step: {name}")


if __name__ == "__main__":
    main()
