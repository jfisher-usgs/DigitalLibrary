## Script (Python) "dateTime"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=name, datetime=None, includeTime=True, cssParent=''
##title=
##
import DateTime

Month = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

if datetime: 
    datetime = DateTime.DateTime(datetime)
    year     = datetime.year()
    month    = datetime.month()
    day      = datetime.day()
    hour     = datetime.hour()
    minute   = datetime.minute()
    second   = datetime.second()
else: year = month = day = hour = minute = second = None

now = DateTime.DateTime()

years   = range(now.year(), 1979, -1)
months  = range(1, 13)
days    = range(1, 32)
hours   = range(24)
minutes = seconds = range(60)

####################################################################

print '<select ' + cssParent + ' name="' + name + '_year">'
if includeTime: print '<option value="">Year</option>'
for i in years:
    if i != year: selected = ''
    else: selected = 'selected'
    print '<option ' + selected + '>' + str(i) + '</option>'
print '</select>'
print ' / '

# month selection

print '<select ' + cssParent + ' name="' + name + '_month">'
if includeTime: print '<option value="">Month</option>'
for i in months:
    if i != month: selected = ''
    else: selected = 'selected'
    print '<option value="' + "%02d" % i + '" ' + selected + '>' + Month[i] + '</option>'
print '</select>'
print ' / '

# day selection

print '<select ' + cssParent + ' name="' + name + '_day">'
if includeTime: print '<option value="">Day</option>'
for i in days:
    if i != day: selected = ''
    else: selected = 'selected'
    print '<option ' + selected + '>' + "%02d" % i + '</option>'
print '</select>'

if includeTime:

    # hour selection

    print '&nbsp;&nbsp;&nbsp;'
    print '<select ' + cssParent + ' name="' + name + '_hour">'
    for i in hours:
        if i != hour: selected = ''
        else: selected = 'selected'
        print '<option ' + selected + '>' + "%02d" % i + '</option>'
    print '</select>'
    print ' : '

    # minute selection

    print '<select ' + cssParent + ' name="' + name + '_minute">'
    for i in minutes:
        if i != minute: selected = ''
        else: selected = 'selected'
        print '<option ' + selected + '>' + "%02d" % i + '</option>'
    print '</select>'
    print ' : '

    # second selection

    print '<select ' + cssParent + ' name="' + name + '_second">'
    for i in seconds:
        if i != second: selected = ''
        else: selected = 'selected'
        print '<option ' + selected + '>' + "%02d" % i + '</option>'
    print '</select>'

return printed
