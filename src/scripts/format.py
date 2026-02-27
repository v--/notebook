# ruff: noqa: S607, PLW1510

import subprocess
import sys


def run_formatters() -> None:
    ruff_proc = subprocess.run(['ruff', 'check', '--fix', *sys.argv[1:]])

    if ruff_proc.returncode != 0:
        raise SystemExit(ruff_proc.returncode)
