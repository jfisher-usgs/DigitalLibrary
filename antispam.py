## Script (Python) "antispam"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=address, mailTo=True
##title=
##
import string
from random import choice

buffer = map(None, address)
for i in range(0, len(address), choice((2,3,4))):
    buffer[i] = '&#%d;' % ord(buffer[i])

val = string.join(buffer,'')

if mailTo == True:
    return '<a href="mailto:%s" class="email">%s</a>' % (val, val)
else:
    return val
