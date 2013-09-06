## Script (Python) "mailForm"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request = container.REQUEST
REQUEST = context.REQUEST

ROOT = container.root()
rootUrl = ROOT.absolute_url()

if REQUEST.form.has_key('users'):
    users = REQUEST.form['users']
else:
    return


val1 = []
for item in users:
    obj = getattr(context, item)
    name = string.join([obj.getProperty('name_first'), obj.getProperty('name_middle'), obj.getProperty('name_last')], ' ')
    val1 += ['"' + name + '" <' + obj.getId() + '>']
val1 = ', '.join(val1)
val2 = ''
val3 = ''

print context.standard_html_header(context, request)

print '<form action="" method="post">'

if REQUEST.form.has_key('sort_on'):
    print '<input type="hidden" name="sort_on"  value="' + REQUEST.form['sort_on']  + '" />'
if REQUEST.form.has_key('sort_dir'):
    print '<input type="hidden" name="sort_dir" value="' + REQUEST.form['sort_dir'] + '" />'
if REQUEST.form.has_key('group_on'):
    print '<input type="hidden" name="group_on" value="' + REQUEST.form['group_on'] + '" />'

print '<h1>Email</h1>'

print '<fieldset>'

print '<ol>'

print '<li>'
print '<label for="recipients">Recipients</label>'
print '<textarea style="width:100%;" rows="2" name="recipients" id="recipients">' + val1 + '</textarea>'
print '</li>'

print '<li>'
print '<label for="subject">Subject</label>'
print '<input style="width:100%;" type="text" name="subject" id="subject" value="' + val2 + '" />'
print '</li>'

print '<li>'
print '<label for="message">Message</label>'
print '<textarea style="width:100%;" rows="6" name="message" id="message">' + val3 + '</textarea>'
print '</li>'

print '</ol>'
print '</fieldset>'

print '<fieldset class="submit">'
print '<input type="submit" name="action" value=" Send " />'
print '<input type="button" value="Cancel" onClick="history.go(-1)" />'
print '</fieldset>'

print '</form>'

print context.standard_html_footer(context, request)

return printed
