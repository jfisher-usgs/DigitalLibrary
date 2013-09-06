## Script (Python) "form_addFolder"
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

publicStatus = ''
if not context.anonymousHasPermission(context):
    publicStatus = 'DISABLED'
    
print context.standard_html_header(context, request)

print '<form action="' + REQUEST['URL1'] + '" method="post" enctype="multipart/form-data">'

print '<h1>New Folder</h1>'

print '<fieldset>'
print '<ol>'

print '<li>'
print '<label for="new_folder">Name</label>'
print '<input type="text" value="" name="new_folder" id="new_folder" size="30" />'
print '<input type="checkbox" name="public_folder" title="Grant anonymous users view/access permissions" ' + publicStatus + ' />Public'
print '<input type="checkbox" name="image_folder" title="Add image gallery" />Image'
print '</li>'

print '</ol>'
print '</fieldset>'

print '<fieldset class="submit">'
print '<input type="submit" name="action" value=" Add " />'
print '<input type="submit" name="action" value="Cancel" />'
print '</fieldset>'

print '</form>'

print '<script type="text/javascript">setDefaultFocus(\'new_folder\');</script>'

print context.standard_html_footer(context, request)

return printed
