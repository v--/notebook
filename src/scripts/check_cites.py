# ruff: noqa: S607, PLW1510

import subprocess


def run_checkcites() -> None:
    proc = subprocess.run(['checkcites', '--backend', 'biber', '--crossrefs', '--all', 'aux/notebook.bcf'])

    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
