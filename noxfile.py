import nox

# Separating Black away from the rest of the sessions
nox.options.sessions = "lint"
code_locations = "common", "src", "test", "util", "noxfile.py"


@nox.session(python="3.6")
def format(session):
    args = session.posargs or code_locations
    session.install("black")
    session.run("black", *args, external=True)


@nox.session(python="3.6")
def lint(session):
    args = session.posargs or code_locations
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python="3.6")
def safety(session):
    session.install("safety")
    session.run("safety", "check", "-r", "requirements.txt", "--full-report")
