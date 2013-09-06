## Script (Python) "form_permissions"
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

if REQUEST.form.has_key('file'):
    objIds = REQUEST.form['file']
else: return

from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()

user = sec_mgr.getUser()
username = user.getUserName()

grpNms = container.people.catalog.uniqueValuesFor('groups')

grpIds = []
for i in range(len(grpNms)):
    grpIds += ['group_' + grpNms[i]]
    
objNams = []
objUrls = []
owners = []
obsers = []
uniqueOwners = []
uniqueObsers = []

folderPresent = False

for i in objIds:
    obj = getattr(context, i)
    
    objNams += [obj.title_or_id()]
    objUrls += [obj.absolute_url(0)]
    
    owner = obj.users_with_local_role('Owner')
    owners += [owner]
    
    obser = obj.users_with_local_role('Observer')
    obsers += [obser]
    
    for i in owner:
        if i not in uniqueOwners:
            uniqueOwners += [i]
            
    for i in obser:
        if i not in uniqueObsers:
            uniqueObsers += [i]
            
    if obj.meta_type in ['Folder', 'Photo Folder']:
        folderPresent = True
        
    if context.anonymousHasPermission(obj):
        publicChk = 'checked="yes"'
    else:
        publicChk = ''
        
users = container.people.filterObjectValues(['Folder'])

usrNms = []
usrIds = []
for i in users:
    usrNm = i.title
    usrId = i.getId()
    if usrId != username:
        usrNms += [usrNm]
        usrIds += [usrId]



####################################################################

print context.standard_html_header(context, request)

print '<h1>Permissions</h1>'

tmp = []
for i in range(len(objNams)):
    tmp = tmp + ['<a href="' + objUrls[i] + '">' + objNams[i] + '</a>']
print '<p>' + '; '.join(tmp) + '</p>'

print '<form method=POST enctype="multipart/form-data">'

for i in objIds: print '<input type="hidden" name="items:list"  value="' + i + '">'
for i in usrIds: print '<input type="hidden" name="users:list"  value="' + i + '">'
for i in grpIds: print '<input type="hidden" name="groups:list" value="' + i + '">'

print '<table border=0>'

print '<tr><th></th><th>Group</th><th>&nbsp;</th><th>User</th><th>&nbsp;</th><th></th></tr>'

#

print '<tr><td align="right">Ownership:</td>'

print '<td><select name="sel_ownGroups:list" size="4" multiple>'
for i in range(len(grpIds)):
    if grpIds[i] in uniqueOwners: selected = 'selected'
    else: selected = ''
    print '<option value="' + grpIds[i] + '" ' + selected + '>' + grpNms[i] + '</option>'
print '</select></td>'

print '<td>&nbsp;</td>'

print '<td><select name="sel_ownUsers:list" size="4" multiple>'
for i in range(len(usrNms)):
    if usrIds[i] in uniqueOwners: selected = 'selected'
    else: selected = ''
    print '<option value="' + usrIds[i] + '" ' + selected + '>' + usrNms[i] + '</option>'
print '</select></td>'

print '<td>&nbsp;</td><td></td></tr>'

#

print '<tr><td align="right">View/Access:</td>'

print '<td><select name="sel_obsGroups:list" size="4" multiple>'
for i in range(len(grpIds)):
    if grpIds[i] in uniqueObsers: selected = 'selected'
    else: selected = ''
    print '<option value="' + grpIds[i] + '" ' + selected + '>' + grpNms[i] + '</option>'
print '</select></td>'

print '<td>&nbsp;</td>'

print '<td><select name="sel_obsUsers:list" size="4" multiple>'
for i in range(len(usrNms)):
    if usrIds[i] in uniqueObsers: selected = 'selected'
    else: selected = ''
    print '<option value="' + usrIds[i] + '" ' + selected + '>' + usrNms[i] + '</option>'
print '</select></td>'

print '<td>&nbsp;</td><td>'
if not context.anonymousHasPermission(context) and folderPresent:
    print '<input type=checkbox name="public" DISABLED />Public'
else:
    print '<input type=checkbox ' + publicChk + ' name="public" title="Grant anonymous users view/access permissions" />Public'
print '</td></tr>'

#

print '<tr><td></td><td colspan="5"><p>'
print '<input type="submit" name="action" value="Save" />'
print '<input type="submit" name="action" value="Cancel" />'
print '<input type="reset" value="Reset" />'
print '</p></td></tr>'

print '</table>'
print '</form>'

print context.standard_html_footer(context, request)

return printed
