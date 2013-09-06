## Script (Python) "form_rename"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request  = container.REQUEST
REQUEST  = context.REQUEST

if REQUEST.form.has_key('file'):
    items = REQUEST.form['file']
else:
    return
    
print context.standard_html_header(context, request)

print '<form action="" method=POST>'

print '<h1>Rename</h1>'

print '<fieldset>'
print '<ol>'

for item in items:
    obj = getattr(context, item)
    val = obj.title_or_id()
    print '<input type="hidden" name="old_name:list" value="' + item + '" />'
    print '<li>'
    print '<label for="new_name">' + val + '</label>'
    print '<input type="text" size="35" name="new_name:list" value="' + val + '" />'
    print '</li>'
    
print '</ol>'
print '</fieldset>'

print '<fieldset class="submit">'
print '<input type="submit" name="action" value="Rename" />'
print '<input type="submit" name="action" value="Cancel" />'
print '</fieldset>'

print '</form>'

print context.standard_html_footer(context,request)

return printed
