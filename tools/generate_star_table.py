#!/usr/bin/env python3
# It is difficult to maintain a table showing the stars collected in Advent of
# Code because the star emoji (:star:) is so wide and there are so many columns,
# so my solution is to create a data table which represents stars with "X" and
# generate a nicely formatted table with this script.

import sys

# File containing star data
STAR_FILE = 'star_table_data.md'
# README file
README_FILE = 'README.md'
# maximum length of a column
MIN_LENGTH = len(':star::star:')
# The lines marking the start and end of the table in the README
TABLE_START_MARKER = '[comment]: # (STAR TABLE START)'
TABLE_END_MARKER = '[comment]: # (STAR TABLE END)'

# Pads out the columns to line up the formatting and replace "X" with ":star:"
def process_line(line, pad_char, min_length):
    result = ''
    # Because we have a '|' at the beginning and end, the first and last
    # character are an empty string and line break respectively, so we discard
    # them
    data = line.split('|')[1:-1]
    # Copy the first column untouched because it is the year column
    result += '|' + data[0] + '|'
    # For each other entry, pad it min_length with the pad_char
    for entry in data[1:]:
        entry = entry.replace('X', ':star:').ljust(min_length, pad_char)
        result += entry + '|'
    # Add line break to make the result a proper line
    result += '\n'
    return result

# Processes each line to generate the processed table
def process_table(star_file):
    result = ''
    with open(star_file, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i == 1:
                # The divider line should be padded with hypens
                result += process_line(line, '-', MIN_LENGTH)
            else:
                result += process_line(line, ' ', MIN_LENGTH)
    return result

# Inserts the processed_table into the readme between the delimeter
def inject_table(readme_file, start_marker, end_marker, table):
    with open(readme_file, 'r+', encoding='utf-8') as file:
        text = file.read()

        # Get the text before the start_marker
        if text.count(start_marker) > 1:
            raise RuntimeError(f'Error: table start marker "{start_marker}" occurs multiple times in "{readme_file}"')
        partition = text.partition(start_marker)
        if partition[1] == '':
            raise RuntimeError(f'Error: table start marker "{start_marker}" not found in "{readme_file}"')
        before = partition[0]

        # Get the text after the end_marker
        if text.count(end_marker) > 1:
            raise RuntimeError(f'Error: table end marker "{end_marker}" occurs multiple times in "{readme_file}"')
        partition = text.partition(end_marker)
        if partition[1] == '':
            raise RuntimeError(f'Error: table end marker "{end_marker}" not found in "{readme_file}"')
        after = partition[2]

        # Insert the table between the markers and write it
        file.seek(0)
        file.truncate(0)
        new_text = before + start_marker + '\n\n' + table + '\n\n' + end_marker + after
        file.write(new_text)

if __name__ == '__main__':
    try:
        processed_table = process_table(STAR_FILE)
    except FileNotFoundError:
        print(f'Error: Could not find star table file "{STAR_FILE}"', file=sys.stderr)
        exit(1)

    try:
        inject_table(README_FILE, TABLE_START_MARKER, TABLE_END_MARKER, processed_table)
    except FileNotFoundError:
        print(f'Error: Could not find README file "{README_FILE}"', file=sys.stderr)
        exit(1)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        exit(1)
