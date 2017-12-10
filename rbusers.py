#!/usr/bin/env python3
""" Print currently logged in users"""
import os
import pwd
import sys

import utmp

USERS = utmp.UtmpRecord()
LOGGED_USERS = {}
# two format strings, to take a/c of users with >10 sessions
FORMAT_STRING_NORM = '%s%s \033[;0m\033[;032m(\033[;033m%d\033[;032m) '
FORMAT_STRING_10 = '%s%s\033[;0m\033[;032m(\033[;033m%d\033[;032m) '
# set colours if we have an encoding
if sys.stdout.encoding is not None:
    DEFAULT_COLOUR = '\033[;0m'
    WHITE_TEXT_ESCAPE = '\033[;035m'
    WHITE_BACK_ESCAPE = '\033[;45m'
    RED_BACK_ESCAPE = '\033[;41m'
    CYAN_BACK_ESCAPE = '\033[;46m'
    GREEN_BACK_ESCAPE = '\033[;42m'
    MAGENTA_BACK_ESCAPE = '\033[;44m'
    YELLOW_BACK_ESCAPE = '\033[;43m'
    GROUPS = {100: '\033[;31m', 107: '\033[;36m',
              108: '\033[;32m', 102: '\033[;33m',
              101: '\033[;34m', 103: '\033[;0m'}
    TITLE_MESSAGE = '\033[;31mTotal \033[;0mNumber \033[;33mof \033[;34mUsers\
                     \033[;35monline\033[;0m:'
else:
    DEFAULT_COLOUR = ''
    WHITE_TEXT_ESCAPE = ''
    WHITE_BACK_ESCAPE = ''
    RED_BACK_ESCAPE = ''
    CYAN_BACK_ESCAPE = ''
    GREEN_BACK_ESCAPE = ''
    MAGENTA_BACK_ESCAPE = ''
    YELLOW_BACK_ESCAPE = ''
    GROUPS = {100: '', 107: '', 108: '', 102: '', 101: '', 103: ''}
    TITLE_MESSAGE = 'Total Number of Users Online:'


def main():
    """ main function """
    # need to deal with .friends
    try:
        friends_file = open(os.path.expanduser('~/.friends'), 'r')
        friends = [i.rstrip() for i in friends_file.readlines()]
    except IOError:
        pass

    # need a dict of users + times logged in
    for user in USERS:
        if user.ut_type == 7:
            seven = user.ut_user
            try:
                LOGGED_USERS[seven][0] = LOGGED_USERS[seven][0] + 1
            except KeyError:
                try:
                    group = pwd.getpwnam(seven)[3]
                    LOGGED_USERS[seven] = [1, ]
                    LOGGED_USERS[seven].append(
                        GROUPS.get(group, DEFAULT_COLOUR))
                    try:
                        if seven in friends and group != 100:
                            LOGGED_USERS[n][1] = white_text_escape
                    except NameError:
                        pass
                except KeyError:
                    pass

    # Alan wants sorted users, so sorted users he shall get
    list_users = list(LOGGED_USERS.keys())
    list_users.sort()

    # printing stuff
    print_users(list_users)


def print_users(list_users):
    """ Pretty Print"""
    print('%s%s%s' %
          ('                         ', TITLE_MESSAGE, len(list_users)))
    print('%s%s%s%s%s%s%s%s%s%s%s%s%s' %
          ('                      ',
           WHITE_BACK_ESCAPE, ' ', DEFAULT_COLOUR, ' friends   ',
           RED_BACK_ESCAPE, ' ', DEFAULT_COLOUR, ' committee  ',
           CYAN_BACK_ESCAPE, ' ', DEFAULT_COLOUR, ' associate'))
    print('%s%s%s%s%s%s%s%s%s%s%s%s%s' %
          ('                      ',
           MAGENTA_BACK_ESCAPE, ' ', DEFAULT_COLOUR, ' society   ',
           YELLOW_BACK_ESCAPE, ' ', DEFAULT_COLOUR, ' club       ',
           GREEN_BACK_ESCAPE, ' ', DEFAULT_COLOUR, ' guest'))
    print()
    print('     ', end=' ')
    # go through and print the users.
    # we only want 5 users for a line which is what iter is for
    itera = 0
    for user in list_users:
        itera = itera + 1
        temp_user = (LOGGED_USERS[user][1], user.ljust(8)[:8],
                     LOGGED_USERS[user][0])
        if LOGGED_USERS[user][0] < 10:
            print(FORMAT_STRING_NORM % temp_user, end=' ')
        else:
            print(FORMAT_STRING_10 % temp_user, end=' ')
        if itera >= 5:
            itera = 0
            print()
            print('     ', end=' ')
    # reset to default colour for stupid terms
    print(DEFAULT_COLOUR)


if __name__ == "__main__":
    main()
