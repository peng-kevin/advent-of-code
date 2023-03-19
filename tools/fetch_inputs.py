#!/usr/bin/env python3

from typing import TextIO
import urllib.request
import os
import sys
import tool_common as common

class colors:
    RESET = '\033[0;0m'
    FETCHED = '\033[0;32m'
    CACHED = '\033[0;32m'
    SKIPPED = '\033[0;90m'


class DirNotFoundError(RuntimeError):
    pass


class FileExistsError(RuntimeError):
    pass


# Prints with color where "color" is an ansi code
def cprint(string: str, color: str, file: TextIO = sys.stdout, end: str = '\n', flush: bool = False) -> None:
    print(f'{color}{string}{colors.RESET}', file=file, end=end, flush=flush)


# Downloads and returns the input for a certain year and day
def fetch_input_text(year: int, day: int, session: str) -> str:
    request = urllib.request.Request(f'https://adventofcode.com/{year}/day/{day}/input')
    request.add_header('Cookie', f'session={session}')
    request.add_header('User-Agent', common.get_user_agent())
    with urllib.request.urlopen(request) as response:
        return response.read().decode('utf-8')


# Downloads and writes the input file
# Only done if the directory for this year and day exists and the input file
# does not exist to avoid sending the server unnecessary requests
def fetch_input_day(year: int, day: int, session: str) -> None:
    input_file_path = common.get_input_file_path(year, day)
    # Check if the folder for the day exists
    if (not os.path.isdir(os.path.dirname(input_file_path))):
        raise DirNotFoundError(f'No such directory: {os.path.dirname(input_file_path)}')
    # Check if the file exists
    if (os.path.exists(input_file_path)):
        raise FileExistsError(f'File exists: {input_file_path}')
    # Download and write the file
    input = fetch_input_text(year, day, session)
    with open(input_file_path, 'w', encoding='utf-8') as file:
        file.write(input)


# Downloads and writes the input files for a year
# Returns true if at least one directory for a day was found, false otherwise
def fetch_input_year(year: int, session: str) -> bool:
    print(f'{year}: ', end='', flush=True)
    no_day_exists = True
    for day in range(1, common.get_num_days() + 1):
        try:
            fetch_input_day(year, day, session)
        except DirNotFoundError:
            cprint(f'.', colors.SKIPPED, end ='', flush=True)
            day_exists = False
        except FileExistsError:
            cprint('-', colors.CACHED, end='', flush=True)
            day_exists = True
        else:
            cprint('X', colors.FETCHED, end='', flush=True)
            day_exists = True
        if day_exists:
            no_day_exists = False
    print("")
    return not no_day_exists


def print_symbol_guide() -> None:
    cprint('.', colors.SKIPPED, end='')
    print(': directory for day does not exist (skipped)')
    cprint('-', colors.CACHED, end='')
    print(': input for day already exists (cached)')
    cprint('X', colors.FETCHED, end='')
    print(': input for day downloaded')


def main() -> None:
    try:
        session_token = common.get_session_token()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)
    except common.EmptySessionFileError as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)

    print_symbol_guide()
    no_day_exists = True
    for year in range(common.get_start_year(), common.get_end_year() + 1):
        if fetch_input_year(year, session_token):
            no_day_exists = False

    if no_day_exists:
        print('No directory for a day was found. Are you running this script from the root of the repository?')


if __name__ == '__main__':
    main()
    
