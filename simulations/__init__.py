"""Utility scripts for running comparative statics simulations.

This package contains helpers that orchestrate experiments on the
``formal_model`` module and persist the resulting datasets for
post-processing. See :mod:`simulations.runner` for the command-line
entry point.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

__all__ = ["run_all_experiments"]


def run_all_experiments(output_dir: Path, run_id: str | None = None) -> List[Path]:
    """Proxy to :func:`simulations.runner.run_all_experiments`.

    The indirection avoids importing :mod:`simulations.runner` during
    package initialization, which prevents ``python -m simulations.runner``
    from emitting a ``RuntimeWarning`` about partially initialized modules.
    """

    from .runner import run_all_experiments as _run

    return _run(output_dir, run_id=run_id)
