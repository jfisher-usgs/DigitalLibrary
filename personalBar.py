## Script (Python) "personalBar"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()

user = sec_mgr.getUser()
username = user.getUserName()

ROOT = container.root()
rootUrl = ROOT.absolute_url()

print '<div id="foot">'

if user.has_role(['Manager'], container) or hasattr(ROOT.people, username):
    print '<a href="' + rootUrl + '/logout">Logout</a>'
    
    if user.has_role(['Manager'], container):
        print '&nbsp;<a href="' + rootUrl + '/manage_main">Zope</a>'
        print '&nbsp;<a href="' + rootUrl + '/files/form_metaFields">Metadata</a>'
        
    else:
        print '&nbsp;<a href="' + rootUrl + '/people/preferences">Preferences</a>'
        
else:
    print '<a href="' + rootUrl + '/login">Login</a>&nbsp;'
    print '<a href="' + rootUrl + '/people/registration">Register</a>'

if string.find(context.REQUEST['HTTP_USER_AGENT'], 'MSIE') < 0:
    print '&nbsp;<a href="' + rootUrl + '/files/maps">Maps</a>'

print '</div>'

return printed
