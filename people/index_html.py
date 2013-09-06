## Script (Python) "index_html"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=People
##
request  = container.REQUEST
REQUEST  = context.REQUEST
RESPONSE = request.RESPONSE

from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()

ROOT = container.root()
rootUrl = ROOT.absolute_url()

user = sec_mgr.getUser()
username = user.getUserName()

if user.has_role(['Manager'], container):
    username = ROOT.getProperty('email')

path = context.absolute_url(0)

access = user.has_role(['Manager', 'chiefs', 'braves'], context)

# Function to change role of user
def changeUserRole(userId, userRole):
    obj = getattr(context, userId)
    oldRole = obj.getProperty('role')
    if userRole != oldRole:
        obj.manage_changeProperties({'role' : userRole})
        groups = context.acl_users.getUser(userId).getGroups()
        role = []
        
        if userRole == 'New Member':
            obj.manage_changeProperties({'groups' : []})
            obj.manage_changeProperties({'manageGroups' : []})
            groups = None
        elif userRole == 'Member':
            obj.manage_changeProperties({'manageGroups' : []})
            role = ['braves']
        elif userRole == 'Manager':
            role = ['chiefs']
            
        context.acl_users.changeUser(userId, groups=groups, roles=role)
        container.catalog.catalog_object(obj)
      # contact the user to inform them of the role change
        snd = username
        rcp = obj.getId()
        msg = 'This email is to inform you of a role change on\n\n' + rootUrl + '\n\nYour user role has gone from ' + oldRole + ' to ' + userRole + '.'
        container.sendMail(recipient=rcp, sender=snd, subject='Role Change', message=msg)

# Function to add users to group
def addUsersToGroup(userIds, group):
    
    grpUsrs = context.acl_users.getMemberIds(groupid=group)
    
    newUsrs = []
    for i in userIds:
        if i not in grpUsrs:
            newUsrs += [i]
    userIds = grpUsrs + newUsrs
    
    context.acl_users.setMembers(groupid=group, userids=userIds)
    
    for i in newUsrs:
        obj = getattr(context, i)
        grps = list(obj.getProperty('groups'))
        role = obj.getProperty('role')
        
        if group not in grps:
            grps += [group]
            obj.manage_changeProperties({'groups' : grps})
            
        if role == 'New Member':
            changeUserRole(i, 'Member')
            
        if role == 'Manager':
            manGrps = list(obj.getProperty('manageGroups'))
            if group not in manGrps:
                manGrps += [group]
                obj.manage_changeProperties({'manageGroups' : manGrps})
                
        container.catalog.catalog_object(obj)

##########################################################################

if REQUEST.form.has_key('action'):
    
  # Add new group
    if REQUEST.form['action'] == ' Add ' and REQUEST.form['new_group'] != '':
        newGrp = REQUEST.form['new_group']
        if newGrp in context.acl_users.getGroupNames():
            raise Exception, 'group_name_in_use'
        context.acl_users.changeOrCreateGroups(groups=[], roles=['braves'], nested_groups=[], new_groups=[newGrp], REQUEST={}, )
        
        if REQUEST.form.has_key('addGroupMembers'):
            userIds = REQUEST.form['addGroupMembers']
            addUsersToGroup(userIds, newGrp)
            
  # Send email
    if REQUEST.form['action'] == ' Send ' and REQUEST.form['recipients'] != '':
        rcp = []
        for i in string.split(REQUEST.form['recipients'], ','):
            rcp += [i[i.find("<")+1:i.find(">")]]
        snd = username
        msg = REQUEST.form['message']
        sbj = REQUEST.form['subject']
        container.sendMail(recipients=rcp, sender=snd, subject=sbj, message=msg)
        
  # Change user role
    if REQUEST.form['action'] == 'Change':
        roles = REQUEST.form['roles']
        userIds= REQUEST.form['userIds']
        for i in range(len(userIds)):
            changeUserRole(userIds[i], roles[i])
            
# Identify selected users
if REQUEST.form.has_key('users'):
    userIds = REQUEST.form['users']
    
# Identify selected group
if REQUEST.form.has_key('group'):
    groupId = REQUEST.form['group']
    
# Delete users
if REQUEST.form.has_key('delUser') and REQUEST.form.has_key('users'):
    context.acl_users.deleteUsers(userIds, REQUEST={})
    for i in userIds:
        obj = getattr(context, i)
        uid = '/'.join(obj.getPhysicalPath())
        container.catalog.uncatalog_object(uid)
      # contact the user to inform them of their membership cancelation
        snd = username
        rcp = obj.getId()
        msg = 'This email is to inform you that your membership has been canceled at\n\n' + rootUrl
        container.sendMail(recipient=rcp, sender=snd, subject='Membership Canceled', message=msg)
    context.manage_delObjects(userIds)
    
# Add users to group
if REQUEST.form.has_key('addUser') and REQUEST.form.has_key('group') and REQUEST.form.has_key('users'):
    if groupId == '':
        return
    addUsersToGroup(userIds, groupId)
    
# Remove users from a group
if REQUEST.form.has_key('rmUser') and REQUEST.form.has_key('group'):
    if groupId == '':
        return
    if REQUEST.form.has_key('users'):
        grpUsrs = context.acl_users.getMemberIds(groupid=groupId)
        rmUsrs = []
        for i in userIds:
            if i in grpUsrs:
                rmUsrs += [i]
                grpUsrs.remove(i)
        context.acl_users.setMembers(groupid=groupId, userids=grpUsrs)
        for i in rmUsrs:
            obj = getattr(context, i)
            grps = []
            for j in list(obj.getProperty('groups')):
                if j != groupId:
                    grps += [j]
            obj.manage_changeProperties({'groups' : grps})
            manGrps = []
            for j in list(obj.getProperty('manageGroups')):
                if j != groupId:
                    manGrps += [j]
            obj.manage_changeProperties({'manageGroups' : manGrps})
            container.catalog.catalog_object(obj)
            
    if context.acl_users.getMemberIds(groupid=groupId) == []:
        context.acl_users.deleteGroups(groups=[groupId], REQUEST={})

##########################################################################

print context.standard_html_header(context, request)

print '<form action="" method="post" id="objectItems">'

sort_on = 'title'
sort_dir = 'asc'
group_on = ''

if REQUEST.form.has_key('sort_on'):
    sort_on = REQUEST.sort_on
if REQUEST.form.has_key('sort_dir'):
    sort_dir = REQUEST.sort_dir
if REQUEST.form.has_key('group_on'):
    group_on = REQUEST.group_on

print '<input type="hidden" name="sort_on"  value="' + sort_on  + '" />'
print '<input type="hidden" name="sort_dir" value="' + sort_dir + '" />'
print '<input type="hidden" name="group_on" value="' + group_on + '" />'

mainPage = True
if context.hasProperty('registered'):
    mainPage = False

if mainPage:
    print '<h1>People</h1>'
    
    if user.has_role(['Manager', 'chiefs'], context):
        print '<div class="documentActions">'
        print '<ul>'
        print '<button class="iconsSys addGroup" type="submit" name="addGroupForm:action" value="" title="Create new group"></button>'
        print '</ul>'
        print '</div>'
        
    oldPath = path + '?sort_on=' + sort_on + '&amp;sort_dir=' + sort_dir
    
    objs = context.filterObjectValues(['Folder'])
    
    if sort_on == 'registered':
        objs = sequence.sort(objs, (('registered', 'cmp', sort_dir),))
    else:
        objs = sequence.sort(objs, ((sort_on, 'nocase', sort_dir),))
        
    print '<table width="100%" cellspacing="0" cellpadding="2">'
    
    print '<tr>'
    
    if access:
        print '<th style="width:1%;">'
        print '<input type="checkbox" id="theController" name="theController" title="Select/unselect all" onclick="toggleSelect(\'objectItems\', \'theController\', \'usersList\')"/>'
        print '</th>'
        
    if group_on != '':
        grpOn = '&amp;group_on=' + group_on
    else:
        grpOn = ''
    
    sortPath = path + '?sort_on=role'
    if sort_on == 'role' and sort_dir == 'asc':
        sortPath += '&amp;sort_dir=desc'
    print '<th style="white-space:nowrap;width:1%;">&nbsp;<a href="' + sortPath + grpOn + '">Role</a>&nbsp;</th>'
    
    sortPath = path + '?sort_on=title'
    if sort_on == 'title' and sort_dir == 'asc':
        sortPath += '&amp;sort_dir=desc'
    print '<th style="width:47%;" align="left"><a href="' + sortPath + grpOn + '">Name</a></th>'
    
    sortPath = path + '?sort_on=registered'
    if sort_on == 'registered' and sort_dir == 'asc':
        sortPath += '&amp;sort_dir=desc'
    print '<th style="width:1%;" align="center"><a href="' + sortPath + grpOn + '">Registered</a>&nbsp;&nbsp;</th>'
    
    sortPath = path + '?sort_on=id'
    if sort_on == 'id' and sort_dir == 'asc':
        sortPath += '&amp;sort_dir=desc'
    print '<th style="width:1%;" align="left"><a href="' + sortPath + grpOn + '">Email</a></th>'
    
    print '<th style="width:49%;" align="left">'
    print '<ul class="menuDrop">'
    print '<li><a class="drop">Groups&nbsp;<small style="font-family: arial;">&#9660;</small><!--[if IE 7]><!--></a><!--<![endif]-->'
    print '<ul>'
    
    if group_on != '': print '<li><a href="' + oldPath + '">All groups</a></li>'
    for i in context.catalog.uniqueValuesFor('groups'):
        if group_on != i:
            grpPath = oldPath + '&amp;group_on=' + i
            print '<li><a href="' + grpPath + '">' + i + '</a></li>'
    
    print '</ul></li></ul></th>'
    print '</tr>'
    
    indx = 0
    for obj in objs:
        
        if obj.getProperty('public') or username == obj.getId() or access:
            
            grps = list(obj.getProperty('groups'))
            if group_on == '' or group_on in grps:
                
                if indx % 2 != 0:
                    print '<tr class="even">'
                else:
                    print '<tr class="odd">'
                indx = indx + 1
                
                title = obj.title
                date  = obj.getProperty('registered').toZone(obj.getProperty('timeZone'))
                email = obj.getId()
                grps  =  ', '.join(sequence.sort(grps))
                role  = obj.getProperty('role')
                
                if access:
                    props = ''
                    if REQUEST.has_key('select'):
                        props = 'CHECKED'
                    print '<td><input type="checkbox" name="users:list" id="usersList" value="' + context.antispam(email, mailTo=False) + '" ' + props + ' /></td>'
                
                link = path + '/' + context.antispam(email, mailTo=False)
                
                print '<td align="center">'
                print '<a href="' + link + '" title="' + role + '" >'
                
                if role == 'Manager':
                    print '<span class="iconsSys manager"></span>'
                elif role == 'Member':
                    print '<span class="iconsSys member"></span>'
                elif role == 'New Member':
                    print '<span class="iconsSys newMember"></span>'
                print '</a></td>'
                
                print '<td>'
                if obj.hasObject('image'):
                    print '<a class="screen" href="' + link + '">' + title + '<b><img src="' + obj.image.absolute_url() + '" width="100" height="100" alt="" /></b></a>'
                else:
                    print '<a href="' + link + '">' + title + '</a>'
                if access and obj.getProperty('public'):
                    print '<span class="iconsSys publicIcon" title="Public">&nbsp;</span>'
                print '</td>'
                
                print '<td style="white-space:nowrap;">'
                print date.Date() + '&nbsp;&nbsp;'
                print '</td>'
                
                print '<td style="white-space:nowrap;">' + context.antispam(email) + '&nbsp;&nbsp;</td>'
                
                print '<td>' + grps + '</td>'
                
                print '</tr>'
                
    print '</table>'
    print '<p></p>'

####

else:
    name = string.join([context.getProperty('name_first'), context.getProperty('name_middle'), context.getProperty('name_last')], ' ')
    
    print '<h1>' + name + '</h1>'
    
    if getattr(context, "image", None) is not None:
        print '<p></p>'
        print '<img src="' + path + '/image" class="logo" width="100" height="100" alt="" />'
    
    print '<fieldset>'
    print '<ol>'
    
    hld = context.getId()
    if hld != '':
        print '<li><label class="noform">Email:</label>' + context.antispam(hld) + '</li>'
        print '<input type="hidden" name="users:list" value="' + context.antispam(hld, mailTo=False) + '" />'
        
    hld = context.getProperty('groups')
    hld = ', '.join(hld)
    if hld != '':
        print '<li><label class="noform">Groups:</label>' + hld + '</li>'
        
    hld = context.getProperty('role')
    if hld != '':
        print '<li><label class="noform">Role:</label>' + hld + '</li>'
    
    hld = context.getProperty('registered').toZone(context.getProperty('timeZone'))
    if hld != '':
        print '<li><label class="noform">Registered&nbsp;on:</label>' + hld.Date() + '</li>'
        
    hld = context.getProperty('organization')
    if hld != '':
        print '<li><label class="noform">Organization:</label>' + hld + '</li>'
        
    hld = context.getProperty('url')
    if hld != '':
        url = hld
        if url[0:4] != 'http':
            url = 'http://' + url
        print '<li><label class="noform">Website:</label><a href="' + url + '" class="addressUrl">' + hld + '</a></li>' 
        
    hld = context.getProperty('interests')
    if hld != '':
        print '<li><label class="noform">Interests:</label>' + hld + '</li>'
        
    print '</ol>'
    print '</fieldset>'

####

print '<fieldset class="submit">'

if access:
    print '<input type="submit" name="mailForm:action" value="Email" />'
    if user.has_role(['Manager', 'chiefs'], context):
        userManages = context.acl_users.getGroupNames()
        if user.has_role(['chiefs'], context):
            obj = getattr(context, username)
            userManages = list(obj.getProperty('manageGroups'))
        print '<input type="submit" name="roleForm:action" value="Role" />'
        if user.has_role(['Manager'], context):
            print '<input type="submit" name="delUser" value="Delete" onClick="return confirmSubmit()" />'
            
if not mainPage:
    if REQUEST.has_key('back'):
        print '<input type="button" value="Return" onClick="history.go(-1)" />'
    else:
        print '<input type="button" value="Return" onClick="parent.location=\'' + REQUEST['URL2'] + '\'" />'

print '</fieldset>'

if user.has_role(['Manager', 'chiefs'], context):
    print '<fieldset class="submit">'
    
    print '<select style="vertical-align:middle" name="group">'
    print '<option value="" >Select group...</option>'
    
    for i in userManages:
        print '<option value="' + i + '">' + i + '</option>'
    print '</select>'
    print '<input type="submit" name="addUser" value="Add" />'
    print '<input type="submit" name="rmUser" value="Remove" />'
    
    print '</fieldset>'

print '</form>'

print context.standard_html_footer(context, request)

return printed
