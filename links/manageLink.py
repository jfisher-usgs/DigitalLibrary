## Script (Python) "manageLink"
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

val = REQUEST.form['manageLink']

if val == 'Add Link':
    name = ''
    category = ''
    url = ''
    description = ''

else:
    obj = getattr(context, val)
    name = obj.getProperty('title')
    category = obj.getProperty('category')
    url = obj.getProperty('url')
    description = obj.getProperty('description') 

catUnique = string.split(REQUEST.form['catUnique'], ";")

###

print context.standard_html_header(context, request)

print '<form action="" method="post">'

if name == '':
    print '<h1>Add Link</h1>'
else:
    print '<h1>Edit Link</h1>'
    print '<input type="hidden" name="id" value="' + obj.getId() + '" />'

print '<fieldset>'

print '<ol>'

print '<li>'
print '<label for="catLink">Category</label>'
print '<input type="text" size="30" name="catLink" id="catLink" value="' + category + '" />'
print '<select name="select_catLink">'
print '<option value="">or choose...</option>'
for i in catUnique:
    print '<option>' + i + '</option>'
print '</select>'
print '</li>'

print '<li>'
print '<label for="namLink">Name</label>'
print '<input type="text" size="30" name="namLink" id="namLink" value="' + name + '" />'
print '</li>'

print '<li>'
print '<label for="urlLink">URL</label>'
print '<input type="text" size="30" name="urlLink" id="urlLink" value="' + url + '" />'
print '</li>'

print '<li>'
print '<label for="desLink">Description</label>'
print '<textarea cols="60" rows="4" name="desLink" id="desLink">' + description + '</textarea>'
print '</li>'

print '</ol>'
print '</fieldset>'

print '<fieldset class="submit">'
if name == '':
    print '<input type="submit" name="action" value="Add" />'
else:
    print '<input type="submit" name="action" value="Save" />'

print '<input type="submit" name="action" value="Cancel" />'

if name != '':
    print '<input type="submit" name="action" value="Delete" />'
print '</fieldset>'

print '</form>'

print context.standard_html_footer(context, request)

return printed
