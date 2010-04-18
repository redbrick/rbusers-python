#!/usr/bin/python
import utmp
import pwd
import os
import sys
users = utmp.UtmpRecord()
logged_users = {}
#two format strings, to take a/c of users with >10 sessions
format_string_norm = '%s%s \033[;0m\033[;032m(\033[;033m%d\033[;032m) '
format_string_10 = '%s%s\033[;0m(%d)'
#set colours if we have an encoding
if sys.stdout.encoding is not None :
    default_colour = '\033[;0m'
    white_text_escape = '\033[;37m'
    white_back_escape = '\033[;47m'
    red_back_escape = '\033[;41m'
    cyan_back_escape = '\033[;46m'
    green_back_escape = '\033[;42m'
    magenta_back_escape = '\033[;45m'
    yellow_back_escape = '\033[;43m'
    groups = { 100 : '\033[;31m', 107 : '\033[;36m', 
    108 : '\033[;32m', 102 : '\033[;33m', 101 : '\033[;35m', 103 : '\033[;0m' }
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
    groups = { 100 : '', 107 : '', 108 : '', 102 : '', 101 : '', 103 : '' }
    title_message = 'Total Number of Users Online:'

#need a dict of users + times logged in
for user in users :
    n = user.ut_user
    try :
        logged_users[n][0] = logged_users[n][0] + 1
    except KeyError :
        try:
            group = pwd.getpwnam(n)[3]
            logged_users[n] = [ 1,  ]
            logged_users[n].append( groups.get( group, default_colour ) )
        except KeyError:
            pass
       
#need to deal with .friends
try :
    friends_file = open( os.path.expanduser('~/.friends'), 'r')
    friends = [ i.rstrip() for i in friends_file.readlines() ]
except IOError :
    pass

#Alan wants sorted users, so sorted users he shall get
list_users = logged_users.keys()
list_users.sort()

#printing stuff
print '%s%s%s' % ('                         ' \
, title_message, len(list_users) )
print '%s%s%s%s%s%s%s%s%s%s%s%s%s' % ( '                      ',
white_back_escape, ' ', default_colour, ' friends   ', 
red_back_escape, ' ', default_colour, ' committee  ',
cyan_back_escape, ' ', default_colour, ' associate' )
print '%s%s%s%s%s%s%s%s%s%s%s%s%s' % ( '                      ', 
magenta_back_escape, ' ', default_colour, ' society   ',
yellow_back_escape, ' ', default_colour, ' club       ',
green_back_escape, ' ', default_colour, ' guest' )
print
print '    ', 


#go through and print the users. 
#we only want 5 users for a line which is what iter is for
iter = 0
for user in list_users :
    iter = iter + 1
    if logged_users[user][0] < 10 :
        print format_string_norm % ( logged_users[user][1],
        user.ljust(8), logged_users[user][0] ),
    else :
        print format_string_10 % ( logged_users[user][1],
        user.ljust(8), logged_users[user][0] ),
    if iter >= 5 :
        iter = 0
        print
        print '    ',
#reset to default colour for stupid terms
print default_colour
