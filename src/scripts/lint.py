# ruff: noqa: S607, PLW1510

import subprocess
import sys


def run_linters() -> None:
    ruff_proc = subprocess.run(['ruff', 'check', *sys.argv[1:]])

    if ruff_proc.returncode != 0:
        raise SystemExit(ruff_proc.returncode)

    mypy_proc = subprocess.run(['mypy', *sys.argv[1:]])

    if mypy_proc.returncode != 0:
        raise SystemExit(mypy_proc.returncode)
