"""CSArts-themed Guessing Game"""

# TODO:
# [ ] Allow player to go back in time
# [ ] Blocklist after each round
# [?] Fix incorrect play in history
# [X] Allow player to choose people

import csv
import time
import random
import argparse
from thefuzz import process

parser = argparse.ArgumentParser(
    prog='main.py',
    description='CSArts Connections Game by Octavia Roberts'
)
parser.add_argument('-a', '--start')
parser.add_argument('-b', '--end')

args = parser.parse_args()
#print(args.start, args.end)

DATA = 'data.csv'

shows = {}
members = {}

blocklist = []
ROUND = 1
STEP = 0
history = {}

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# populates shows from csv
with open(DATA, mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        # empty cell is falsy, so can be sorted out by if statement
        shows[row[0]] = [name for name in row[1:] if name]

# populates members from shows
for show, show_cast in shows.items():
    for member in show_cast:
        if member in members:
            members[member].append(show)
        else:
            members[member] = [show]

person_a = process.extractOne(args.start, list(members.keys()))[0] if args.start else random.choice(list(members.keys()))
person_b = process.extractOne(args.end, list(members.keys()))[0] if args.end else random.choice(list(members.keys()))

#def play_round(cursor, match_array):
#    RESULT = False
#    while RESULT is False:
#        output = process.extractOne(input('→ '), list(match_array.keys()))
#        RESULT = output[0] in members[cursor] and output[0] not in blocklist
#        color = {True: GREEN, False: RED}[RESULT]
#        print('\033[F' + '→ ' + color + output[0] + RESET)
#    STEP += 1
#    cursor = output[0]
#    history[STEP] = cursor

def phase(cursor, valid_options, lookup_dict, condition=lambda x: True):
    result = False
    while result is False:
        output = process.extractOne(input('→ '), list(valid_options))
        result = output[0] in lookup_dict[cursor] and condition(output[0])
        color = {True: GREEN, False: RED}[result]
        print('\033[F' + '→ ' + color + output[0] + RESET)
    return output[0]

if __name__ == '__main__':
    while True:
        print(f'Round {ROUND}', '\n')
        print('Connect the following people:')
        print(f'{person_a} → {person_b}', '\n')
        ROUND += 1
        history[0] = person_a

        if blocklist:
            print('Without using the following:')
            for i in blocklist:
                print(i)
            print(f'{len(blocklist)} in blocklist')
            print()

        print(person_a)

        cursor = person_a
        while cursor != person_b:
            if cursor is not person_a:
                blocklist.append(cursor)
            # Person phase
            cursor = phase(cursor, shows.keys(), members, lambda o: o not in blocklist)
            STEP += 1
            history[STEP] = cursor
            # Show phase
            cursor = phase(cursor, members.keys(), shows)
            STEP += 1
            history[STEP] = cursor

        STEPS = len(history)-2
        print('\n' + f'You won in {STEPS} step{'s'[:STEPS^1]}!')
        print(' → '.join(map(str,[step for _, step in history.items()])), '\n')

        person_cursor = person_a
