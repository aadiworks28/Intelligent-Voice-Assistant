from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama (important on macOS)
init(autoreset=True)

ASSISTANT_NAME = "Zara"

def timestamp():
    return datetime.now().strftime("%H:%M:%S")


def system_msg(text):
    print(
        f"{Fore.CYAN}[{timestamp()}] System:{Style.RESET_ALL} {text}"
    )


def user_says(text):
    print(
        f"{Fore.GREEN}[{timestamp()}] You:{Style.RESET_ALL} {text}"
    )


def assistant_says(text):
    print(
        f"{Fore.MAGENTA}[{timestamp()}] {ASSISTANT_NAME}:{Style.RESET_ALL} {text}"
    )

