"""CSArts-themed Guessing Game"""

# TODO:
# [ ] Allow player to go back in time
# [X] Blocklist after each round
# [X] Fix incorrect play in history
# [X] Allow player to choose people

import sys
import csv
import random
import argparse
import requests
from thefuzz import process

parser = argparse.ArgumentParser(
    prog='main.py',
    description='CSArts Connections Game by Octavia Roberts'
)
parser.add_argument('-a', '--start')
parser.add_argument('-b', '--end')

args = parser.parse_args()

shows = {}
members = {}

blocklist = []
ROUND = 1

GREEN = '\033[92m'
GREY = '\033[30m'
RED = '\033[91m'
RESET = '\033[0m'

DATA = 'data.csv'
URL = "https://raw.githubusercontent.com/risograph/csarts-connected/refs/heads/main/data.csv"
r = requests.get(URL)
url_data = r.content.decode('UTF-8')
local_data = open(DATA,'r',encoding='UTF-8').read()
if url_data != local_data:
    print(GREEN + 'An update is available!' + RESET)
    print(GREY + 'Updating show data...' + RESET)
    o = open('old_data.csv','w',encoding='UTF-8')
    o.write(local_data)
    f = open(DATA,'w',encoding='UTF-8')
    f.write(url_data)
    print('\033[F' + GREEN + 'Done updating!                ' + RESET)
    print(GREY + 'Please rerun the game to play.' + RESET)
    sys.exit()

# populates shows from csv
with open(DATA,'r',encoding='UTF-8') as infile:
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

def phase(cursor, valid_options, lookup_dict, condition=lambda x: True):
    result = False
    while result is False:
        user_input = input('→ ')
        if user_input.lower() == 'exit':
            print(GREY + 'See you soon!' + RESET)
            sys.exit()
        output = process.extractOne(user_input, list(valid_options))
        result = output[0] in lookup_dict[cursor] and condition(output[0])
        color = {True: GREEN, False: RED}[result]
        print('\033[F' + '→ ' + color + output[0] + RESET)
    return output[0]

if __name__ == '__main__':
    while True:
        STEP = 0
        history = {}
        print('\n' + f'Round {ROUND}')
        print(GREY + 'Connect the following people:' + RESET)
        print(f'{person_a} → {person_b}', '\n')
        ROUND += 1
        history[0] = person_a

        if blocklist:
            print(GREY + 'Without using the following:' + RESET)
            for i in sorted(blocklist):
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

        cursor = person_a
