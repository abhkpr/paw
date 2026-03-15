"""git operations for paw"""

import subprocess


def is_git_repo() -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True
    )
    return result.returncode == 0


def has_staged_changes() -> bool:
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        capture_output=True
    )
    return result.returncode == 1


def get_staged_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "--cached", "--stat", "--patch"],
        capture_output=True, text=True
    )
    return result.stdout


def get_staged_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True
    )
    return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]


def do_commit(message: str) -> bool:
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stderr)
        return False
    print(result.stdout)
    return True
