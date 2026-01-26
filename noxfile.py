import nox
import os
from laminci import upload_docs_artifact
from laminci.nox import build_docs, run_pre_commit, run, install_lamindb

IS_PR = os.getenv("GITHUB_EVENT_NAME") != "push"

# we'd like to aggregate coverage information across sessions
# and for this the code needs to be located in the same
# directory in every github action runner
# this also allows to break out an installation section
nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session()
def build(session, group):
    branch = "main" if IS_PR else "release"
    install_lamindb(session, branch=branch)
    run(session, "pytest -s ./tests/test_notebooks.py")
    build_docs(session, strict=False)
    upload_docs_artifact(aws=True)
