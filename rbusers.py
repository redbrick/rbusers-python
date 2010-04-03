#!/usr/bin/python
import utmp
import sys
import fcntl
import termios
import struct
import os
import pwd
users = utmp.UtmpRecord()
logged_users = {}
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
for user in users :
    n = user.ut_user
    try :
        pwd.getpwnam(n)
        try :
            logged_users[n] = logged_users[n] + 1
        except KeyError:
            logged_users[n] = 1
    except KeyError:
        pass
friends_file = open( os.path.expanduser('~/.friends'), 'r')
friends = [ i.rstrip() for i in friends_file.readlines() ]
#http://old.nabble.com/Unable-to-see-os.environ-%27COLUMNS%27--td19487200.html
print '%s%s%s' % ('                         ' \
, title_message, len(logged_users) )
print '%s%s%s%s%s%s%s' % ( '                      ',\
white_back_escape, ' \033[;0m friends   ', \
red_back_escape, ' \033[;0m committee  ',\
cyan_back_escape, ' \033[;0m associate' )
print '%s%s%s%s%s%s%s' % ( '                      ', \
magenta_back_escape, ' \033[;0m society   ',\
yellow_back_escape, ' \033[;0m club       ',\
green_back_escape, ' \033[;0m guest' )
print
iter = 0
print '    ', 
for user in logged_users.keys() :
    iter = iter + 1
    if user in friends :
        print ' %s%s (%d)' %\
        (white_text_escape, user.ljust(8), logged_users[user] ),
    else :
        try :
            group = pwd.getpwnam(user)[3]
            print ' %s%s (%d)' % ( groups[group], user.ljust(8), logged_users[user] ),
        except KeyError:
            print ' %s%s (%d)' % ( default_colour, user.ljust(8), logged_users[user] ), 
    if iter >= 5 :
        iter = 0
        print
        print '    ',
