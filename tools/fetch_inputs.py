#!/usr/bin/env python3

import urllib.request
import os


# Which days to get inputs for 
START_YEAR = 2015
END_YEAR = 2022
NUM_DAYS = 25

USER_AGENT = 'https://github.com/peng-kevin/advent-of-code by kevinpeng02@gmail.com'
INPUT_FILENAME = 'input.txt'

SESSION_FILE = 'session.txt'


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
        return
    # Check if the file exists
    if (os.path.exists(input_file_path)):
        return
    # Download and write the file
    input = fetch_input_text(year, day, session)
    with open(input_file_path, 'w', encoding='utf-8') as file:
        file.write(input)


# Downloads and writes the input files for a year
def fetch_input_year(year, session):
    for day in range(1, NUM_DAYS + 1):
        fetch_input_day(year, day, session)


# Gets the session token from session.txt
def get_session_token():
    with open(SESSION_FILE) as file:
        return file.read().strip()

if __name__ == '__main__':
    for year in range(START_YEAR, END_YEAR + 1):
        fetch_input_year(year, get_session_token())
