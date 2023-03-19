#!/usr/bin/env python3

from pathlib import Path
import urllib.request
import sys
import tool_common as common

class colors:
    RESET = '\033[0;0m'
    FETCHED = '\033[0;32m'
    CACHED = '\033[0;32m'
    SKIPPED = '\033[0;90m'


def fetch_answer_text(year: int, day: int, session: str) -> str:
    request = urllib.request.Request(f'https://adventofcode.com/{year}/day/{day}/input')
    request.add_header('Cookie', f'session={session}')
    request.add_header('User-Agent', common.get_user_agent())
    with urllib.request.urlopen(request) as response:
        text = response.read().decode('utf-8')
    print(text)


def main():
    try:
        session_token = get_session_token(SESSION_FILE)
    except FileNotFoundError:
        print(f'Error: session file "{SESSION_FILE}" not found. This file should contain your session token for fetching input. The file has been created in the current directory.', file=sys.stderr)
        Path(SESSION_FILE).touch()
        exit(1)
    if session_token == '':
        print(f'Error: session file "{SESSION_FILE}" is empty. This file should contain your session token for fetching input', file=sys.stderr)
        exit(1)

    print_symbol_guide()
    no_day_exists = True
    for year in range(START_YEAR, END_YEAR + 1):
        if fetch_input_year(year, session_token):
            no_day_exists = False

    if no_day_exists:
        print('No directory for a day was found. Are you running this script from the root of the repository?')


if __name__ == '__main__':
    main()
