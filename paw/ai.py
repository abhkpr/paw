"""AI commit message generation via ollama"""

import re
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

COMMIT_TYPES = ["feat", "fix", "docs", "style", "refactor", "test", "chore", "perf"]

SYSTEM_PROMPT = """You are an expert developer who writes clean, precise git commit messages.
You follow the Conventional Commits specification exactly.

Format:
<type>(<optional scope>): <short description>

<optional body — explain WHY not WHAT, max 3 lines>

Rules:
- type must be one of: feat, fix, docs, style, refactor, test, chore, perf
- description must be lowercase, no period at end, max 72 chars
- use imperative mood: "add feature" not "added feature"
- body is optional — only include if the change needs explanation
- NEVER include anything except the commit message
- NO markdown, NO backticks, NO explanation, NO preamble
- output ONLY the commit message, nothing else"""


def build_prompt(diff: str, force_type: str = None, no_body: bool = False) -> str:
    max_diff_len = 4000
    if len(diff) > max_diff_len:
        diff = diff[:max_diff_len] + "\n\n[diff truncated]"

    type_instruction = ""
    if force_type:
        type_instruction = f"\nYou MUST use '{force_type}' as the commit type.\n"

    body_instruction = ""
    if no_body:
        body_instruction = "\nWrite ONLY the subject line. No body.\n"

    return f"""Analyze this git diff and write a conventional commit message for it.
{type_instruction}{body_instruction}
Git diff:
{diff}

Write the commit message now:"""


def generate_commit_message(
    diff: str,
    model: str = "codellama",
    force_type: str = None,
    no_body: bool = False
) -> str:
    prompt = build_prompt(diff, force_type, no_body)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "system": SYSTEM_PROMPT,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "num_predict": 256,
                }
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        message = data.get("response", "").strip()
        return clean_message(message)

    except requests.exceptions.ConnectionError:
        print("\n  error: cannot connect to ollama")
        print("  make sure ollama is running: ollama serve")
        return None
    except requests.exceptions.Timeout:
        print("\n  error: ollama timed out")
        return None
    except Exception as e:
        print(f"\n  error: {e}")
        return None


def clean_message(message: str) -> str:
    message = re.sub(r"```[a-z]*\n?", "", message)
    message = message.strip("`").strip()

    lines = message.strip().split("\n")
    cleaned = []
    started = False
    for line in lines:
        if not started:
            if any(line.strip().startswith(f"{t}") for t in COMMIT_TYPES):
                started = True
                cleaned.append(line)
        else:
            cleaned.append(line)

    if cleaned:
        return "\n".join(cleaned).strip()

    return message.strip()
