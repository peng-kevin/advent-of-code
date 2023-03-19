from os import path

# Which days to get answers for 
START_YEAR = 2015
END_YEAR = 2022
NUM_DAYS = 25

USER_AGENT = 'https://github.com/peng-kevin/advent-of-code by kevinpeng02@gmail.com'
ANSWER_FILENAME = 'answer.txt'
INPUT_FILENAME = 'input.txt'

SESSION_FILE = 'session.txt'


class EmptySessionFileError(RuntimeError):
    pass


def get_answer_file_path(year, day) -> str:
    """Returns the expected path for the input file of a certain year and day"""
    return path.join('src', str(year), f'day{str(day).zfill(2)}', ANSWER_FILENAME)


def get_input_file_path(year, day) -> str:
    """Returns the expected path for the input file of a certain year and day"""
    return path.join('src', str(year), f'day{str(day).zfill(2)}', INPUT_FILENAME)


def get_user_agent() -> str:
    """Returns the user agent string for http communication"""
    return USER_AGENT


def get_start_year() -> int:
    return START_YEAR


def get_end_year() -> int:
    return END_YEAR


def get_num_days() -> int:
    return NUM_DAYS


def get_session_token() -> str:
    """Returns the session token used to communicate with Advent of Code server"""
    with open(SESSION_FILE) as file:
        try:
            session_token = file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f'session file "{SESSION_FILE}" not found. This file should contain your session token for fetching input')
    if session_token == '':
        raise EmptySessionFileError(f'session file "{SESSION_FILE}" is empty. This file should contain your session token for fetching input')
    return session_token


