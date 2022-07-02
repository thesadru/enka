"""Nox file."""
from __future__ import annotations

import logging
import pathlib
import typing

import nox

nox.options.sessions = ["reformat", "lint", "type-check", "verify-types"]
nox.options.reuse_existing_virtualenvs = True
PACKAGE = "shinshin"
GENERAL_TARGETS = ["./shinshin", "./noxfile.py"]
PYRIGHT_ENV = {"PYRIGHT_PYTHON_FORCE_VERSION": "latest"}

LOGGER = logging.getLogger("nox")


def isverbose() -> bool:
    """Whether the verbose flag is set."""
    return LOGGER.getEffectiveLevel() == logging.DEBUG - 1


def verbose_args() -> typing.Sequence[str]:
    """Return --verbose if the verbose flag is set."""
    return ["--verbose"] if isverbose() else []


def install_requirements(session: nox.Session, *requirements: str, literal: bool = False) -> None:
    """Install requirements."""
    if not literal and all(requirement.isalpha() for requirement in requirements):
        files = ["requirements.txt"]
        files += [f"./dev-requirements/{requirement}-requirements.txt" for requirement in requirements]
        requirements = tuple(arg for file in files for arg in ("-r", file))

    session.install("--upgrade", "pip", *requirements, silent=not isverbose())


@nox.session()
def lint(session: nox.Session) -> None:
    """Run this project's modules against the pre-defined flake8 linters."""
    install_requirements(session, "lint")
    session.run("flake8", "--version")
    session.run("flake8", *GENERAL_TARGETS, *verbose_args())
    session.run("python", "-m", "slotscheck", "-m", PACKAGE, *verbose_args())


@nox.session()
def reformat(session: nox.Session) -> None:
    """Reformat this project's modules to fit the standard style."""
    install_requirements(session, "reformat")
    session.run("black", *GENERAL_TARGETS, *verbose_args())
    session.run("isort", *GENERAL_TARGETS, *verbose_args())

    session.log("sort-all")
    LOGGER.disabled = True
    session.run("sort-all", *map(str, pathlib.Path(PACKAGE).glob("**/*.py")), success_codes=[0, 1])
    LOGGER.disabled = False


@nox.session(name="type-check")
def type_check(session: nox.Session) -> None:
    """Statically analyse and veirfy this project using pyright and mypy."""
    install_requirements(session, "typecheck")
    session.run("pyright", PACKAGE, *verbose_args(), env=PYRIGHT_ENV)


@nox.session(name="verify-types")
def verify_types(session: nox.Session) -> None:
    """Verify the "type completeness" of types exported by the library using pyright."""
    install_requirements(session, ".", "--force-reinstall", "--no-deps")
    install_requirements(session, "typecheck")

    session.run("pyright", "--verifytypes", PACKAGE, "--ignoreexternal", *verbose_args(), env=PYRIGHT_ENV)
