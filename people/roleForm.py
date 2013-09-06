## Script (Python) "roleForm"
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
user = sec_mgr.getUser()

ROOT = container.root()
rootUrl = ROOT.absolute_url()

if REQUEST.form.has_key('users'):
    users = REQUEST.form['users']
else:
    return

#######################################################

print context.standard_html_header(context, request)

print '<form action="" method="post">'

if REQUEST.form.has_key('sort_on'):
    print '<input type="hidden" name="sort_on"  value="' + REQUEST.form['sort_on']  + '" />'
if REQUEST.form.has_key('sort_dir'):
    print '<input type="hidden" name="sort_dir" value="' + REQUEST.form['sort_dir'] + '" />'
if REQUEST.form.has_key('group_on'):
    print '<input type="hidden" name="group_on" value="' + REQUEST.form['group_on'] + '" />'

print '<h1>Role</h1>'

print '<fieldset>'
print '<ol>'

for item in users:
    print '<input type="hidden" name="userIds:list" value="' + item + '" />'
    
    obj = getattr(context, item)
    print '<li>'
    
    name = string.join([obj.getProperty('name_first'), obj.getProperty('name_middle'), obj.getProperty('name_last')], ' ')
    print '<label for="roles">' + name + '</label>'
    
    role = obj.getProperty('role')
    
    disRoles = []
    if not user.has_role(['Manager'], container):
        if role == 'Manager':
            disRoles += ['New Member', 'Member']
        else:
            disRoles += ['Manager']
            
    print '<select style="width:10em;" name="roles:list">'
    for i in ['New Member', 'Member', 'Manager']:
        if i == role:
            selected = 'selected="selected"'
        else:
            selected = ''
        
        if i not in disRoles: 
            print '<option ' + selected + ' value="' + i + '">' + i + '</option>'
    print '</select>'
    print '</li>'
    
print '</ol>'
print '</fieldset>'

print '<fieldset class="submit">'
print '<input type="submit" name="action" value="Change" />'
print '<input type="submit" name="action" value="Cancel" />'
print '<input type="reset" value="Reset" />'
print '</fieldset>'

print '<span class="formHelp">An email will be sent informing the user(s) of their role change.</span>'

print '</form>'

print context.standard_html_footer(context, request)

return printed
