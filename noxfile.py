import nox

# Separating Black away from the rest of the sessions
nox.options.sessions = "lint", "safety", "tests"
code_locations = "datagateway_api", "test", "util", "noxfile.py"


@nox.session(reuse_venv=True)
def black(session):
    args = session.posargs or code_locations

    session.run("poetry", "install", "--only=dev", external=True)
    session.run("black", *args, external=True)


@nox.session(reuse_venv=True)
def lint(session):
    args = session.posargs or code_locations
    session.run("poetry", "install", "--only=dev", external=True)
    session.run("flake8", *args)


@nox.session(reuse_venv=True)
def safety(session):
    session.install("safety")
    # Ignore vulnerabilities as the patched versions of dependencies that they
    # relate to don't support Python 3.6 which is still required for production
    session.run(
        "safety",
        "check",
        "--full-report",
    )


@nox.session(python=["3.11"], reuse_venv=True)
def unit_tests(session):
    args = session.posargs
    session.run("poetry", "install", external=True)
    session.run("pytest", "test/unit", *args)


@nox.session(python=["3.11"], reuse_venv=True)
def integration_tests(session):
    args = session.posargs
    session.run("poetry", "install", external=True)
    session.run("pytest", "test/integration", *args)
