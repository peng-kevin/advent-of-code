#!/usr/bin/env python3

import urllib.request
import os
import sys


# Which days to get inputs for 
START_YEAR = 2015
END_YEAR = 2022
NUM_DAYS = 25

USER_AGENT = 'https://github.com/peng-kevin/advent-of-code by kevinpeng02@gmail.com'
INPUT_FILENAME = 'input.txt'

SESSION_FILE = 'session.txt'


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
def cprint(string, color, file=sys.stdout, end='\n', flush=False):
    print(f'{color}{string}{colors.RESET}', file=file, end=end, flush=flush)

# Downloads and returns the input for a certain year and day
def fetch_input_text(year, day, session):
    request = urllib.request.Request(f'https://adventofcode.com/{year}/day/{day}/input')
    request.add_header('Cookie', f'session={session}')
    request.add_header('User-Agent', USER_AGENT)
    with urllib.request.urlopen(request) as response:
        return response.read().decode('utf-8')


# Returns the expected path for the input file of a certain year and day
def get_input_file_path(year, day):
    return os.path.join(str(year), 'src', f'day{str(day).zfill(2)}', INPUT_FILENAME)


# Downloads and writes the input file
# Only done if the directory for this year and day exists and the input file
# does not exist to avoid sending the server unnecessary requests
def fetch_input_day(year, day, session):
    input_file_path = get_input_file_path(year, day)
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
def fetch_input_year(year, session):
    print(f'{year}: ', end='', flush=True)
    no_day_exists = True
    for day in range(1, NUM_DAYS + 1):
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


# Gets the session token from session.txt
def get_session_token(session_file):
    with open(session_file) as file:
        return file.read().strip()


def print_symbol_guide():
    cprint('.', colors.SKIPPED, end='')
    print(': directory for day does not exist (skipped)')
    cprint('-', colors.CACHED, end='')
    print(': input for day already exists (cached)')
    cprint('X', colors.FETCHED, end='')
    print(': input for day downloaded')

if __name__ == '__main__':
    try:
        session_token = get_session_token(SESSION_FILE)
    except FileNotFoundError:
        print(f'Error: session file "{SESSION_FILE}" not found. This file should contain your session token for fetching input', file=sys.stderr)
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
    
