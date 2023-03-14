"""Nox sessions."""

import tempfile
from typing import Any

import nox
from nox.sessions import Session


nox.options.sessions = "black", "mypy"
locations = "src", "noxfile.py"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--format",
            "requirements.txt",
            "--with",
            "dev",
            "--without-hashes",
            "--output",
            f"{requirements.name}",
            external=True,
        )
        session.install("--requirement", f"{requirements.name}", *args, **kwargs)


@nox.session(python="3.9")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.9")
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)