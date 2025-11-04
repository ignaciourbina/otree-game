#!/usr/bin/env python3
"""Run repeated bot sessions for the AI growth risk experiment."""

from __future__ import annotations

import argparse
import contextlib
import importlib
import json
import logging
import os
import sys
from pathlib import Path
from typing import Iterable

LOGGER = logging.getLogger(__name__)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Spin up oTree bot sessions for the ai_growth_risk experiment to "
            "stress test randomised scenarios and payouts."
        )
    )
    parser.add_argument(
        "--settings-module",
        default="testing.settings_bots",
        help="Dotted path to the oTree settings module to import.",
    )
    parser.add_argument(
        "--session-config",
        default="ai_growth_risk_bot",
        help="Session config name to instantiate for each run.",
    )
    parser.add_argument(
        "--participants",
        type=int,
        default=2,
        help="Number of participants to include in each session.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=5,
        help="How many sequential bot sessions to execute.",
    )
    parser.add_argument(
        "--random-seed-base",
        type=int,
        help="Optional base value used to deterministically vary treatment seeds by iteration.",
    )
    parser.add_argument(
        "--export-dir",
        type=Path,
        help="If provided, export wide CSV logs for each run into this directory.",
    )
    parser.add_argument(
        "--verbosity",
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="Logging verbosity for the harness itself.",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


@contextlib.contextmanager
def use_project_environment(settings_module: str) -> Iterable[None]:
    repo_root = Path(__file__).resolve().parents[1]
    project_root = repo_root / "projects" / "custom_apps"
    os.environ.setdefault("OTREE_SETTINGS_MODULE", settings_module)
    # oTree insists on importing a module literally named "settings" from CWD.
    # We temporarily chdir into the custom project package and register the
    # requested settings module under that canonical name.
    prev_cwd = Path.cwd()
    prev_settings = sys.modules.get("settings")
    try:
        os.chdir(project_root)
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        settings_module_obj = importlib.import_module(settings_module)
        sys.modules["settings"] = settings_module_obj
        yield settings_module_obj
    finally:
        os.chdir(prev_cwd)
        if prev_settings is not None:
            sys.modules["settings"] = prev_settings
        else:
            sys.modules.pop("settings", None)


def ensure_static_scaffolding():
    """Provide the minimal folder structure expected by oTree imports."""
    repo_root = Path(__file__).resolve().parents[1]
    for root in (repo_root, repo_root / "projects" / "custom_apps"):
        static_dir = root / "_static"
        static_dir.mkdir(exist_ok=True)


def bootstrap_database(app_model_modules: Iterable[str]):
    """Initialise the SQLAlchemy session used by oTree."""
    import importlib

    import otree.models  # noqa: F401
    import otree.models_concrete  # noqa: F401
    from otree.cli.resetdb import Command
    from otree.database import AnyModel, db, engine

    for module_name in app_model_modules:
        importlib.import_module(module_name)

    # Reset the schema so that stress runs start from a clean database.
    Command().handle(interactive=False)
    AnyModel.metadata.create_all(engine)
    db.new_session()


def export_session_data(session, destination: Path) -> None:
    from otree import export as otree_export

    destination.mkdir(parents=True, exist_ok=True)
    run_dir = destination

    session_code = session.code
    with (run_dir / "all_apps_wide.csv").open("w", encoding="utf8") as fp:
        otree_export.export_wide(fp, session_code=session_code)

    for app_name in session.config["app_sequence"]:
        safe_name = app_name.replace(".", "_")
        with (run_dir / f"{safe_name}.csv").open("w", encoding="utf8", newline="") as fp:
            otree_export.export_app(app_name, fp)



def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.verbosity.upper()))
    ensure_static_scaffolding()

    with use_project_environment(args.settings_module):
        from otree.session import SESSION_CONFIGS_DICT, create_session
        config = SESSION_CONFIGS_DICT[args.session_config]
        app_model_modules = [f"{app_name}.models" for app_name in config["app_sequence"]]

        bootstrap_database(app_model_modules)
        from otree.bots.runner import run_bots

        for iteration in range(args.iterations):
            seed = None
            if args.random_seed_base is not None:
                seed = args.random_seed_base + iteration

            modified_fields = {"random_seed": seed} if seed is not None else None
            if modified_fields:
                LOGGER.info(
                    "Starting iteration %s with random_seed=%s", iteration + 1, seed
                )
            else:
                LOGGER.info("Starting iteration %s", iteration + 1)

            session = create_session(
                args.session_config,
                num_participants=args.participants,
                modified_session_config_fields=modified_fields,
            )
            run_bots(session.id)

            if args.export_dir:
                run_folder = args.export_dir / f"run_{iteration + 1:03d}"
                export_session_data(session, run_folder)

            # Record key outcomes for quick inspection without opening the DB.
            summary = {
                "iteration": iteration + 1,
                "session_code": session.code,
                "scenario_labels": [
                    group.scenario_label for group in session.get_groups()
                ],
                "collective_runtime": [
                    group.collective_runtime for group in session.get_groups()
                ],
            }
            LOGGER.info("Session summary: %s", json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
