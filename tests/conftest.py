import pytest

SAMPLE_WORKFLOW = """
name: Tests
on: push
jobs:
  tests:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
        python-version: ["3.6", "3.7", "3.8", "3.9", "3.10"]
    name: Tests with Python ${{ matrix.python-version }} on ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
          architecture: x64

      - run: pip install nox
      - run: pip install poetry

      - name: Run nox on Linux
        run: nox

      - name: Publish coverage metrics
        run: nox -rs coverage
        if: startsWith(matrix.os, 'ubuntu')
        env:
          CODECOV_TOKEN: ${{secrets.CODECOV_TOKEN}}
"""


@pytest.fixture
def sample_workflow(tmp_path):
    wf_path = tmp_path / ".github" / "workflows"
    wf_path.mkdir(parents=True)
    wf_file = wf_path / "tests.yaml"
    wf_file.write_text(SAMPLE_WORKFLOW)

    yield wf_file
