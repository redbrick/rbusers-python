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
friend_colour = '\033[;37m'
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
,'\033[;31mTotal \033[;0mNumber \033[;33mof \033[;34mUsers \033[;35monline\033[;0m:', len(logged_users) )
print '%s%s%s' % ( '                      ', '\033[;47m \033[;0m friends', \
'   \033[;41m \033[;0m committee   \033[;46m \033[;0m associate' )
print '%s%s%s%s' % ( '                      ', \
'\033[;45m \033[;0m society   ',\
'\033[;43m \033[;0m club        ',\
'\033[;42m \033[;0m guest' )
print
groups = { 100 : '\033[;31m', 107 : '\033[;36m', \
108 : '\033[;32m', 102 : '\033[;33m', 101 : '\033[;35m' }
iter = 0
print '    ', 
for user in logged_users.keys() :
    iter = iter + 1
    if user in friends :
        print ' %s%s (%d)' % (friend_colour, user.ljust(8), logged_users[user] ),
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
