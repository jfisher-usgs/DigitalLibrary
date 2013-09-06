## Script (Python) "form_addLink"
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

print '<h1>New Link</h1>'

print '<fieldset>'
print '<ol>'

print '<li>'
print '<label for="new_link_name">Name</label>'
print '<input type="text" value="" name="new_link_name" id="new_link_name" size="30" />'
print '<input type="checkbox" name="public_link" title="Grant anonymous users view/access permissions" ' + publicStatus + ' />Public'
print '</li>'

print '<li>'
print '<label for="new_link_url">URL</label>'
print '<input type="text" value="" name="new_link_url" id="new_link_url" size="30" />'
print '</li>'

print '</ol>'
print '</fieldset>'

print '<fieldset class="submit">'
print '<input type="submit" name="action" value=" Add " />'
print '<input type="submit" name="action" value="Cancel" />'
print '</fieldset>'

print '</form>'

print '<script type="text/javascript">setDefaultFocus(\'new_link_name\');</script>'

print context.standard_html_footer(context, request)

return printed
