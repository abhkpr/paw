"""terminal UI for paw"""

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
MUTED  = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def print_banner():
    print(f"\n{GREEN}{BOLD}paw{RESET}{MUTED} — local AI commit message generator{RESET}\n")


def print_message(message: str):
    lines = message.strip().split("\n")
    width = max(len(line) for line in lines) + 4
    width = max(width, 40)

    print(f"\n{CYAN}┌{'─' * width}┐{RESET}")
    for i, line in enumerate(lines):
        if i == 0:
            print(f"{CYAN}│{RESET}  {BOLD}{line}{RESET}{' ' * (width - len(line) - 2)}{CYAN}│{RESET}")
        elif line.strip() == "":
            print(f"{CYAN}│{RESET}{' ' * width}{CYAN}│{RESET}")
        else:
            print(f"{CYAN}│{RESET}  {MUTED}{line}{RESET}{' ' * (width - len(line) - 2)}{CYAN}│{RESET}")
    print(f"{CYAN}└{'─' * width}┘{RESET}\n")


def ask_confirm() -> str:
    print(f"  {GREEN}y{RESET} commit    {YELLOW}r{RESET} regenerate    {CYAN}e{RESET} edit    {MUTED}n{RESET} abort")
    print()
    while True:
        try:
            choice = input(f"  {MUTED}→{RESET} ").strip().lower()
            if choice in ("y", "r", "e", "n", ""):
                return choice if choice else "y"
        except KeyboardInterrupt:
            print()
            return "n"


def print_error(msg: str):
    print(f"\n  {RED}✗{RESET} {msg}\n")


def print_success(msg: str):
    print(f"\n  {GREEN}✓{RESET} {msg}\n")


def print_info(msg: str):
    print(f"  {MUTED}→{RESET} {msg}")
