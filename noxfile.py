import tempfile

import nox

# Separating Black away from the rest of the sessions
nox.options.sessions = "lint", "safety"
code_locations = "datagateway_api", "test", "util", "noxfile.py"


def install_with_constraints(session, req_dir=None, *args, **kwargs):
    with tempfile.NamedTemporaryFile(dir=req_dir) as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


def get_tmp_dir(session):
    tmp_dir = None

    try:
        if session.posargs[-2] == "--tmpdir":
            tmp_dir = session.posargs.pop(-1)
            session.posargs.remove("--tmpdir")
    except IndexError:
        session.log("Info: No --tmpdir option given")

    return tmp_dir


@nox.session(python="3.6", reuse_venv=True)
def black(session):
    tmp_dir = get_tmp_dir(session)
    args = session.posargs or code_locations

    install_with_constraints(session, tmp_dir, "black")
    session.run("black", *args, external=True)


@nox.session(python="3.6", reuse_venv=True)
def lint(session):
    tmp_dir = get_tmp_dir(session)
    args = session.posargs or code_locations
    install_with_constraints(
        session,
        tmp_dir,
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-broken-line",
        "flake8-bugbear",
        "flake8-builtins",
        "flake8-commas",
        "flake8-comprehensions",
        "flake8-import-order",
        "flake8-logging-format",
        "pep8-naming",
    )
    session.run("flake8", *args)


@nox.session(python="3.6", reuse_venv=True)
def safety(session):
    tmp_dir = get_tmp_dir(session)
    install_with_constraints(session, tmp_dir, "safety")
    with tempfile.NamedTemporaryFile(dir=tmp_dir) as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=["3.6", "3.7", "3.8"], reuse_venv=True)
def tests(session):
    args = session.posargs
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
