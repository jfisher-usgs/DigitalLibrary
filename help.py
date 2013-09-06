## Script (Python) "help"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=key, typ=None
##title=
##
val1 = val2 = val3 = None

if key == 'Metadata':
    if   typ == 'boolean': 
        val1 = 'Enter a boolean value. '
        val2 = '0 or 1'
    elif typ == 'float': 
        val1 = 'Enter a decimal number. '
        val2 = '3.14159'
    elif typ == 'int': 
        val1 = 'Enter an integer value. '
        val2 = '12'
    elif typ == 'date': 
        val1 = 'Select the year, month, day, hour, minute, and second from the drop-down lists. '
    elif typ == 'lines': 
        val1 = 'Enter a list of strings separated by semicolons. If available, previously cataloged values may be added using selections from the scrollable list. You can select multiple values by holding down the appropriate modifier key (Ctrl on Windows). '
        val2 = 'item 1; item 2; item 3'
    elif typ == 'string': 
        val1 = 'Enter a string of characters. '
        val2 = 'this is a string'
    elif typ == 'text': 
        val1 = 'Enter a multi-line string. '
    elif typ == 'tokens': 
        val1 = 'Enter a list of strings seperated by white space. '
        val2 = 'one two three'
    elif typ == 'owner':
        val1 = 'Select an item from the scrollable list. You can select multiple values by holding down the appropriate modifier key (Ctrl on Windows). Granting a user <i>Owner</i> permissions on a file gives them the ability to edit metadata, copy/paste, public/private, delete, etc. Contact the site administrator to revoke a users <i>Owner</i> permissions. '

if key == 'Search':
    if   typ == 'boolean': 
        val1 = 'Enter a boolean value. '
        val2 = '0 or 1'
    elif typ == 'float': 
        val1 = 'Enter a decimal number. '
        val2 = '3.14159'
    elif typ == 'int': 
        val1 = 'Enter an integer value. '
        val2 = '12'
    elif typ == 'date': 
        val1 = 'Select the year, month, and day from the drop-down lists. '
    elif typ == 'lines': 
        val1 = 'Select an item from the drop-down list. '
    elif typ == 'text': 
        val1 = 'Enter a string of characters. Valid boolean operators include AND, OR, and NOT. Wild cards (* and ?) are also allowed. '
        val2 = '((word1 AND word2) OR word3)'
    elif typ in ['string', 'tokens']: 
        val1 = 'Enter a string of characters. '
        val2 = 'word1'
    if typ in ['date', 'int', 'float']:
        val1 += 'Specify the range of the search by selecting before or after from the drop-down list. '

msg = ''
if key in ['Metadata', 'Search']:
    if val1: msg += val1
    if val2: msg += 'Example: ' + val2

return msg
