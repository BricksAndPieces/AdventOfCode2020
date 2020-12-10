from urllib.request import urlopen
import urllib.request
from os import path
import ssl
import sys

# Avoid certificate issues (OK because only accessing AOC)
ssl._create_default_https_context = ssl._create_unverified_context
project_path = path.dirname(path.abspath(__file__))


def create_day_file(day, year):
    with open(project_path + '/template.txt', 'r') as file:
        template = file.read()

    template = template.replace('DAY', f'{day}').replace('YEAR', f'{year}')
    with open(project_path + f'/{year}/days/day{day:02d}.py', 'w') as file:
        file.write(template)


def puzzle_input(day, year='2020'):
    file_path = f'{project_path}/{year}/inputs/day{day:02d}.txt'
    if not path.exists(file_path) or path.getsize(file_path) == 0:
        print('Downloading Input...')
        opener = urllib.request.build_opener()
        opener.addheaders.append(('Cookie', f'session={__get_cookie()}'))
        url = f'https://adventofcode.com/{year}/day/{day}/input'
        print(url)
        page = opener.open(url)

        with open(file_path, 'w') as file:
            file.write(page.read().decode('utf-8').strip())

    with open(file_path, 'r') as file:
        return file.read()


def __get_cookie(file='/cookie.txt'):
    with open(project_path + file, 'r') as file:
        return file.read()


def ints(str_array, split='\n'):
    return [int(s) for s in str_array.split(split)]


def iterate_char(c: str):
    return chr(ord(c) + 1) if c.lower() != 'z' else 'a' if c.islower() else 'A'


def cache(func, key=lambda args: args):
    mem = dict()

    def memoized_func(*args):
        k = key(args)
        if k in mem:
            return mem[k]
        result = func(*args)
        mem[k] = result
        return result

    return memoized_func


"""
Allows the user to create a python file for a puzzle based of the day and year
This is run if aoc.py is called from the command line to speed up creation of day files
"""
if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        create_day_file(int(sys.argv[1]), sys.argv[2])
    except:
        print('Please provide a day and year')
        print('Ex. python3 aoc.py 5 2020')
