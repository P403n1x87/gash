from pathlib import Path

from gash._workflow import Workflow


def test_workflow(sample_workflow):
    wf = Workflow(sample_workflow)
    assert wf._data
    assert wf.path == sample_workflow
    assert wf.name == "Tests"
