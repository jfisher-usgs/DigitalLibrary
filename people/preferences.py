## Script (Python) "preferences"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
import DateTime

ROOT = container.root()

timeZones = (
'Brazil/Acre', 'Brazil/DeNoronha', 'Brazil/East', 'Brazil/West', 
'Canada/Atlantic', 'Canada/Central', 'Canada/East-Saskatchewan', 'Canada/Mountain', 'Canada/Newfoundland', 'Canada/Pacific', 'Canada/Yukon', 'Chile/Continental', 'Chile/EasterIsland', 
'Cuba', 
'Egypt', 
'GB-Eire', 
'GMT', 
'GMT+0', 'GMT+0130','GMT+0230','GMT+0330', 'GMT+0430', 'GMT+0530', 'GMT+0630', 'GMT+0730', 'GMT+0830', 'GMT+0930', 
'GMT+1', 'GMT+10', 'GMT+1030', 'GMT+11', 'GMT+1130', 'GMT+12', 'GMT+1230', 'GMT+13', 
'GMT+2', 'GMT+3', 'GMT+4', 'GMT+5', 'GMT+6', 'GMT+7', 'GMT+8', 'GMT+9', 
'GMT-0130', 'GMT-0230', 'GMT-0330', 'GMT-0430', 'GMT-0530', 'GMT-0630', 'GMT-0730', 'GMT-0830', 'GMT-0930', 
'GMT-1', 'GMT-10', 'GMT-1030', 'GMT-11', 'GMT-1130', 'GMT-12', 'GMT-1230', 
'GMT-2', 'GMT-3', 'GMT-4', 'GMT-5', 'GMT-6', 'GMT-7', 'GMT-8', 'GMT-9', 
'Greenwich', 
'Hongkong', 
'Iceland', 
'Iran', 
'Israel', 
'Jamaica', 
'Japan', 
'Mexico/BajaNorte', 'Mexico/BajaSur', 'Mexico/General', 
'Poland', 
'Singapore', 
'US/Alaska','US/Aleutian', 'US/Arizona', 'US/East-Indiana', 'US/Eastern', 'US/Hawaii','US/Indiana-Starke', 'US/Michigan', 'US/Mountain', 'US/Pacific', 'US/Samoa', 
'Universal'
)

request  = container.REQUEST
REQUEST  = context.REQUEST

from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()

user = sec_mgr.getUser()
username = user.getUserName()

results = context.catalog({'id' : username, 'meta_type' : 'Folder'})
userobj = getattr(context, results[0].id)

if REQUEST.form.has_key('action'):
    
    fname        = REQUEST.form['fname']
    mname        = REQUEST.form['mname']
    lname        = REQUEST.form['lname']
    url          = REQUEST.form['url']
    organization = REQUEST.form['organization']
    interests    = REQUEST.form['interests']
    portrait     = REQUEST.form['portrait']
    timeZone     = REQUEST.form['timeZone']
    
    if REQUEST.form.has_key('public'):
        public = 1
    else:
        public = 0
    
    if mname != '':
        name = "%s, %s %s" % (lname, fname, mname)
    else:
        name = "%s, %s" % (lname, fname)
    
    userobj.manage_changeProperties(title=name)
    
    userobj.manage_changeProperties(name_first=fname)
    userobj.manage_changeProperties(name_middle=mname)
    userobj.manage_changeProperties(name_last=lname)
    
    userobj.manage_changeProperties(url=url)
    userobj.manage_changeProperties(organization=organization)
    userobj.manage_changeProperties(interests=interests)
    userobj.manage_changeProperties(timeZone=timeZone)
    userobj.manage_changeProperties(public=public)

    context.catalog.uncatalog_object(userobj)
    context.catalog.catalog_object(userobj)

    if REQUEST.form.has_key('portrait'):
        if portrait.filename != '':
            if "image" in userobj.objectIds(): 
                userobj.manage_delObjects("image")
	    userobj.manage_addImage(id="image", file=portrait.read())

if REQUEST.form.has_key('del'):
    if "image" in userobj.objectIds(): userobj.manage_delObjects("image")


#################

print container.standard_html_header(context, request)

print '<form action="" method="post" enctype="multipart/form-data">'

print '<h1>Preferences</h1>'

print '<fieldset>'

print '<ol>'

print '<li>'
print '<label for="fname">First Name</label>'
print '<input type="text" size="30" name="fname" id="fname" value="' + userobj.name_first + '" />'
print '</li>'

print '<li>'
print '<label for="mname">Middle Initial</label>'
print '<input type="text" size="30" name="mname" id="mname" value="' + userobj.name_middle + '" />'
print '</li>'

print '<li>'
print '<label for="lname">Last Name</label>'
print '<input type="text" size="30" name="lname" id="lname" value="' + userobj.name_last + '" />'
print '</li>'

print '<li>'
print '<label for="url">Website</label>'
print '<input type="text" size="30" name="url" id="url" value="' + userobj.url + '" />'
print '</li>'

print '<li>'
print '<label for="organization">Organization</label>'
print '<input type="text" size="30" name="organization" id="organization" value="' + userobj.organization + '" />'
print '</li>'

print '<li>'
print '<label for="interests">Research Interests <span class="comment">(html tags allowed)</span></label>'
print '<textarea rows="4" cols="60" name="interests" id="interests">' + userobj.interests + '</textarea>'
print '</li>'

print '<li>'
print '<label for="portrait">Portrait <span class="comment">(100 &#215; 100, <a href="http://mypictr.com/?size=100x100" target="_new" title="A picture resizing service">create</a>)</span></label>'
print '<input type="file" size="30" name="portrait" id="portrait" />'
if "image" in userobj.objectIds():
    print '<br />'
    print '<img src="' + userobj.absolute_url(0) + '/image" class="logo" width="100" height="100" alt="" style="padding:0.2em 0 0.2em 0.5em;" />'
    print '<a href="' + container.preferences.absolute_url(0) + '?del=yes" title="Remove portrait"><span class="iconsSys deleteIcon"></span></a>'
print '</li>'
    
print '<li>'
print '<label for="timeZone">Time Zone</label>'
print '<select name="timeZone" id="timeZone">'
if userobj.timeZone != '':
    timezone = userobj.timeZone
else:
    timezone = ROOT.getProperty('timeZone')
for i in timeZones:
    if i == timezone:
        selected = 'selected'
    else:
        selected = ''
    print '<option ' + selected + ' value="' + i + '">' + i + '</option>'
print '</select>'
print '</li>'

print '<li>'
print '<label for="public">Public <span class="comment">(grant anonymous users view permissions)</span></label>'
checked = ''
if userobj.public != 0:
    checked = 'checked="checked"'
print '<input type="checkbox" name="public" id="public" ' + checked + ' />'
print '</li>'

print '</ol>'
print '</fieldset>'

print '<fieldset class="submit">'
print '<input type="submit" name="action" value=" Save " />'
print '<input type="reset" value=" Reset " />'
print '</fieldset>'

print '</form>'

print container.standard_html_footer(context, request)

return printed
