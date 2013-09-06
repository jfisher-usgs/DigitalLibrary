## Script (Python) "addGroupForm"
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

from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()

addGroupMembers = []
if REQUEST.form.has_key('users'):
    addGroupMembers = REQUEST.form['users']
    
user = sec_mgr.getUser()
username = user.getUserName()
if username not in addGroupMembers and not user.has_role(['Manager'], container):
    addGroupMembers += [username]
    
print context.standard_html_header(context, request)

print '<form action="' + REQUEST['URL1'] + '" method="post" enctype="multipart/form-data">'

print '<h1>Add Group</h1>'

print '<fieldset>'
print '<ol>'

print '<li>'
print '<label for="new_group">Name</label>'
print '<input type="text" value="" name="new_group" id="new_group" size="30" />'
print '</li>'

if addGroupMembers != []:
    groupManagers = []
    groupMembers = []
    for i in addGroupMembers:
        print '<input type="hidden" name="addGroupMembers:list" value="' + i  + '" />'
        obj = getattr(context, i)
        name = string.join([obj.getProperty('name_first'), obj.getProperty('name_middle'), obj.getProperty('name_last')], ' ')
        
        if obj.getProperty('role') == 'Manager':
            groupManagers += [name]
        else:
            groupMembers += [name]
            
    if groupManagers != []:
        print '<li><label class="noform">Group&nbsp;Managers:</label>' + string.join(groupManagers, ', ') + '</li>'
    if groupMembers != []:
        print '<li><label class="noform">Group&nbsp;Members:</label>' + string.join(groupMembers, ', ') + '</li>'

print '</ol>'
print '</fieldset>'

print '<fieldset class="submit">'
print '<input type="submit" name="action" value=" Add " />'
print '<input type="submit" name="action" value="Cancel" />'
print '</fieldset>'

for i in addGroupMembers:
    print '<input type="hidden" name="addGroupMembers:list" value="' + i  + '" />'
    
print '</form>'

print '<script type="text/javascript">setDefaultFocus(\'new_group\');</script>'

print context.standard_html_footer(context, request)

return printed
