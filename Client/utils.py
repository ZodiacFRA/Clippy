import time
import random
import re


def get_random_nickname():
    words = open("/usr/share/dict/words").read().splitlines()
    return f'{random.choice(words).capitalize()} {random.choice(words).capitalize()}'


def is_valid_ipv4_address(host):
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?):([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$'''
    if re.search(regex, host):
        print(host)
        dots_idx = host.rfind(':')
        return (host[:dots_idx], int(host[dots_idx + 1:]))


class Pos(object):
    def __init__(s, y, x):
        s.y = y
        s.x = x

    def __add__(s, other):
        if isinstance(other, Pos):
            return Pos(s.y + other.y, s.x + other.x)
        return Pos(s.y + other, s.x + other)

    def __sub__(s, other):
        if isinstance(other, Pos):
            return Pos(s.y - other.y, s.x - other.x)
        return Pos(s.y + other, s.x + other)

    def __floordiv__(s, factor):
        return Pos(s.y // factor, s.x // factor)

    def __truediv__(s, factor):
        return Pos(s.y / factor, s.x / factor)

    def __repr__(s):
        return f"Pos y={s.y}/x={s.x}"

    def __eq__(s, other):
        return s.y == other.y and s.x == other.x

    def __gt__(s, other):
        return s.y > other.y or s.x > other.x

    def __lt__(s, other):
        return s.y < other.y or s.x < other.x

    def __mul__(s, other):
        if isinstance(other, Pos):
            return Pos(s.y * other.y, s.x * other.x)
        return Pos(s.y * other, s.x * other)

    def get_xy(s):
        return (s.x, s.y)

    def __hash__(s):
        ### WARNING, THE HASH SHOULD NEVER CHANGE DURING LIFETIME ###
        return hash(f'{s.y}|{s.x}')


def exit_error(msg):
    print(msg)
    exit()


def log_to_file(msg):
    with open('./log.txt', 'w') as f:
        f.write(f"{time.time()}:\t{msg}\n")


def get_random_unicode_from_range(ranges_list, length=1):
    """ Receives a list of tuples (list of (range_start, range_end))
    returns {length} chars at random from this range """
    try:
        get_char = unichr
    except NameError:
        get_char = chr
    res = ""
    for i in range(length):
        selected_range = random.choice(ranges_list)
        res += get_char(random.randint(*selected_range))
    return res
