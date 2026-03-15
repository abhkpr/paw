#!/usr/bin/env python3
"""paw — local AI commit message generator"""

import sys
import argparse
from .git import get_staged_diff, do_commit, is_git_repo, has_staged_changes
from .ai import generate_commit_message
from .ui import print_banner, print_message, ask_confirm, print_error, print_success, print_info


def main():
    parser = argparse.ArgumentParser(
        prog="paw",
        description="local AI commit message generator using ollama"
    )
    parser.add_argument("--dry", "-d", action="store_true",
        help="print generated message without committing")
    parser.add_argument("--model", "-m", default="codellama",
        help="ollama model to use (default: codellama)")
    parser.add_argument("--type", "-t",
        choices=["feat", "fix", "docs", "style", "refactor", "test", "chore", "perf"],
        help="force a specific conventional commit type")
    parser.add_argument("--no-body", action="store_true",
        help="generate subject line only, no body")
    parser.add_argument("--version", "-v", action="version", version="paw 0.1.0")

    args = parser.parse_args()

    print_banner()

    if not is_git_repo():
        print_error("not a git repository")
        sys.exit(1)

    if not has_staged_changes():
        print_error("no staged changes found")
        print_info("stage your changes first: git add <files>")
        sys.exit(1)

    print_info("reading staged changes...")
    diff = get_staged_diff()

    if not diff.strip():
        print_error("staged diff is empty")
        sys.exit(1)

    print_info(f"generating commit message using {args.model}...")

    while True:
        message = generate_commit_message(
            diff=diff,
            model=args.model,
            force_type=args.type,
            no_body=args.no_body
        )

        if not message:
            print_error("failed to generate commit message")
            sys.exit(1)

        print_message(message)

        if args.dry:
            print_info("dry run — not committing")
            sys.exit(0)

        choice = ask_confirm()

        if choice == "y":
            do_commit(message)
            print_success("committed successfully")
            break
        elif choice == "r":
            print_info("regenerating...")
            continue
        elif choice == "e":
            import tempfile, os, subprocess
            editor = os.environ.get("EDITOR", "nano")
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
                f.write(message)
                tmpfile = f.name
            subprocess.call([editor, tmpfile])
            with open(tmpfile) as f:
                message = f.read().strip()
            os.unlink(tmpfile)
            if message:
                do_commit(message)
                print_success("committed successfully")
            break
        elif choice == "n":
            print_info("aborted")
            break


if __name__ == "__main__":
    main()
