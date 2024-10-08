import os
import tempfile

import nox

# Separating Black away from the rest of the sessions
nox.options.sessions = "lint", "safety", "tests"
code_locations = "datagateway_api", "test", "util", "noxfile.py"


def install_with_constraints(session, *args, **kwargs):
    # Auto file deletion is turned off to prevent a PermissionError experienced on
    # Windows
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)

        try:
            # Due to delete=False, the file must be deleted manually
            requirements.close()
            os.unlink(requirements.name)
        except IOError:
            session.log("Error: The temporary requirements file could not be closed")


@nox.session(reuse_venv=True)
def black(session):
    args = session.posargs or code_locations

    install_with_constraints(session, "black")
    session.run("black", *args, external=True)


@nox.session(reuse_venv=True)
def lint(session):
    args = session.posargs or code_locations
    install_with_constraints(
        session,
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


@nox.session(reuse_venv=True)
def safety(session):
    install_with_constraints(session, "safety")
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        # Ignore vulnerabilities as the patched versions of dependencies that they
        # relate to don't support Python 3.6 which is still required for production
        session.run(
            "safety",
            "check",
            f"--file={requirements.name}",
            "--full-report",
            "--ignore",
            "50916",
            "--ignore",
            "51457",
            "--ignore",
            "51668",
            "--ignore",
            "52322",
            "--ignore",
            "52518",
            "--ignore",
            "53325",
            "--ignore",
            "53326",
            "--ignore",
            "54456",
            "--ignore",
            "55261",
            "--ignore",
            "58910",
            "--ignore",
            "58755",
            "--ignore",
            "59062",
            "--ignore",
            "59473",
            "--ignore",
            "60223",
            "--ignore",
            "60224",
            "--ignore",
            "60225",
            "--ignore",
            "60350",
            "--ignore",
            "60789",
            "--ignore",
            "60841",
            "--ignore",
            "61416",
            "--ignore",
            "62019",
            "--ignore",
            "62151",
            "--ignore",
            "62451",
            "--ignore",
            "62452",
            "--ignore",
            "62556",
            "--ignore",
            "63687",
            "--ignore",
            "64121",
            "--ignore",
            "64227",
            "--ignore",
            "65212",
            "--ignore",
            "64484",
            "--ignore",
            "65278",
            "--ignore",
            "65510",
            "--ignore",
            "65647",
            "--ignore",
            "66704",
            "--ignore",
            "66777",
            "--ignore",
            "67892",
            "--ignore",
            "70612",
            "--ignore",
            "70624",
            "--ignore",
            "70790",
            "--ignore",
            "70982",
            "--ignore",
            "70993",
            "--ignore",
            "71064",
            "--ignore",
            "71083",
            "--ignore",
            "71219",
            "--ignore",
            "71590",
            "--ignore",
            "71591",
            "--ignore",
            "71594",
            "--ignore",
            "71595",
            "--ignore",
            "71680",
            "--ignore",
            "71681",
            "--ignore",
            "71684",
            "--ignore",
            "72132",
            "--ignore",
            "72731",
            "--ignore",
            "72981",
        )

        try:
            # Due to delete=False, the file must be deleted manually
            requirements.close()
            os.unlink(requirements.name)
        except IOError:
            session.log("Error: The temporary requirements file could not be closed")


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10"], reuse_venv=True)
def unit_tests(session):
    args = session.posargs
    # Explicitly installing/downgrading setuptools is done to fix poetry install on 3.8+
    # as per https://github.com/pypa/setuptools/issues/4483#issuecomment-2236327987.
    # A cleaner fix would be to upgrade the packaging library to 22.0+ (as per
    # https://github.com/pypa/setuptools/issues/4483#issuecomment-2236339726) but this
    # cannot be done on this repo until support for Python 3.6 is dropped
    if session.python in ["3.8", "3.9", "3.10"]:
        session.run("pip", "install", "--upgrade", "setuptools==70.0.0")
    session.run("poetry", "install", external=True)
    session.run("pytest", "test/unit", *args)


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10"], reuse_venv=True)
def integration_tests(session):
    args = session.posargs
    # Explicit downgrade of setuptools also performed here. See explanation in
    # `unit_tests()`
    if session.python in ["3.8", "3.9", "3.10"]:
        session.run("pip", "install", "--upgrade", "setuptools==70.0.0")
    session.run("poetry", "install", external=True)
    session.run("pytest", "test/integration", *args)
