#!/usr/bin/python
import utmp
import pwd
import os
import sys
import curses
users = utmp.UtmpRecord()
logged_users = {}
format_string_norm = '%s%s (%d)'
format_string_10 = '%s%s(%d)'
if sys.stdout.encoding is not None :
    default_colour = '\033[;0m'
    white_text_escape = '\033[;37m'
    white_back_escape = '\033[;47m'
    red_back_escape = '\033[;41m'
    cyan_back_escape = '\033[;46m'
    green_back_escape = '\033[;42m'
    magenta_back_escape = '\033[;45m'
    yellow_back_escape = '\033[;43m'
    groups = { 100 : '\033[;31m', 107 : '\033[;36m', \
    108 : '\033[;32m', 102 : '\033[;33m', 101 : '\033[;35m' }
    title_message = '\033[;31mTotal \033[;0mNumber \033[;33mof \033[;34mUsers \033[;35monline\033[;0m:'
else :
    default_colour = ''
    white_text_escape = ''
    white_back_escape = ''
    red_back_escape = ''
    cyan_back_escape = ''
    green_back_escape = ''
    magenta_back_escape = ''
    yellow_back_escape = ''
    groups = { 100 : '', 107 : '', 108 : '', 102 : '', 101 : '' }
    title_message = 'Total Number of Users Online:'
for user in users :
    n = user.ut_user
    try :
        logged_users[n] = logged_users[n] + 1
    except KeyError:
        logged_users[n] = 1
friends_file = open( os.path.expanduser('~/.friends'), 'r')
friends = [ i.rstrip() for i in friends_file.readlines() ]
print '%s%s%s' % ('                         ' \
, title_message, len(logged_users) )
print '%s%s%s%s%s%s%s%s%s%s%s%s%s' % ( '                      ',
white_back_escape, ' ', default_colour, ' friends   ', 
red_back_escape, ' ', default_colour, ' committee  ',
cyan_back_escape, ' ', default_colour, ' associate' )
print '%s%s%s%s%s%s%s%s%s%s%s%s%s' % ( '                      ', 
magenta_back_escape, ' ', default_colour, ' society   ',
yellow_back_escape, ' ', default_colour, ' club       ',
green_back_escape, ' ', default_colour, ' guest' )
print
iter = 0
print '    ', 
for user in logged_users.keys() :
    iter = iter + 1
    if user in friends :
        if logged_users[user] < 10 :
            print format_string_norm %\
            (white_text_escape, user.ljust(8), logged_users[user] ),
        else :
            print format_string_10 %\
            (white_text_escape, user.ljust(8), logged_users[user] ),
    else :
        try :
            group = pwd.getpwnam(user)[3]
            try :
                if logged_users[user] < 10 :
                    print format_string_norm % ( groups[group], user.ljust(8),
                    logged_users[user] ),
                else :
                    print format_string_10 % (groups[group], user.ljust(8),
                    logged_users[user] ),
            except KeyError:
                if logged_users[user] < 10 :
                    print format_string_norm % ( default_colour, user.ljust(8),
                    logged_users[user] ), 
                else :
                    print format_string_10 % ( default_colour, user.ljust(8),
                    logged_users[user] ), 
        except KeyError:
            iter = iter - 1
    if iter >= 5 :
        iter = 0
        print
        print '    ',
