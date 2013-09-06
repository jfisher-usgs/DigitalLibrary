## Script (Python) "string2id"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=s
##title=
##
import string

tt = '______________________________________________._0123456789_______ABCDEFGHIJKLMNOPQRSTUVWXYZ______abcdefghijklmnopqrstuvwxyz_____________________________________________________________________________________________________________________________________'

# translate most things to underscore and remove punctuation
s = string.translate(s, tt, '!@#$%^&*()-=+,\'"')

# remove all double-underscores
while s.find("__") > -1:
    s = s.replace('__','_')
 
# trim underscores off front
s = s.strip("_")

return s
