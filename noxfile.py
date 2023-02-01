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
        # Ignore 50916 as the latest version of pydantic and
        # Ignore 51457 as the latest version of pytest and
        # Ignore 51668 as the latest version of SQLAchemy and
        # Ignore 52355 and 52518 as the latest version of gitpython
        # as they do not support
        # python 3.6 which is still used in production
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
    # Installing setuptools that will work with `2to3` which is used when building
    # `python-icat` < 1.0. 58.0.0 removes support of this tool during builds:
    # https://setuptools.pypa.io/en/latest/history.html#v58-0-0
    # Ideally this would be done within `pyproject.toml` but specifying `setuptools` as
    # a dependency requires Poetry 1.2:
    # https://github.com/python-poetry/poetry/issues/4511#issuecomment-922420457
    # Currently, only a pre-release exists for Poetry 1.2. Testing on the pre-release
    # version didn't fix the `2to3` issue when building Python ICAT, perhaps because
    # Python ICAT isn't built on the downgraded version for some reason?
    session.run("pip", "uninstall", "-y", "setuptools")
    # Not using `poetry run` as it errors on Windows OS when a version with the '<'
    # sign is specified for a package
    session.run("pip", "install", "setuptools<58.0.0")
    session.run("poetry", "install", external=True)
    session.run("pytest", "test/unit", *args)


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10"], reuse_venv=True)
def integration_tests(session):
    args = session.posargs
    # Installing setuptools that will work with `2to3` which is used when building
    # `python-icat` < 1.0. 58.0.0 removes support of this tool during builds:
    # https://setuptools.pypa.io/en/latest/history.html#v58-0-0
    # Ideally this would be done within `pyproject.toml` but specifying `setuptools` as
    # a dependency requires Poetry 1.2:
    # https://github.com/python-poetry/poetry/issues/4511#issuecomment-922420457
    # Currently, only a pre-release exists for Poetry 1.2. Testing on the pre-release
    # version didn't fix the `2to3` issue when building Python ICAT, perhaps because
    # Python ICAT isn't built on the downgraded version for some reason?
    session.run("pip", "uninstall", "-y", "setuptools")
    # Not using `poetry run` as it errors on Windows OS when a version with the '<'
    # sign is specified for a package
    session.run("pip", "install", "setuptools<58.0.0")
    session.run("poetry", "install", external=True)
    session.run("pytest", "test/integration", *args)
