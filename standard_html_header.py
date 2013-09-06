## Script (Python) "standard_html_header"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=*args, **kwargs
##title=
##
from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()

user = sec_mgr.getUser()
username = user.getUserName()

ROOT = container.root()
rootUrl = ROOT.absolute_url()

apiKey = container.getProperty('googleMapsApiKey')

print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
print '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'

print '<head>'
print '<base href="' + rootUrl + '/" />'
print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
print '<title>' + container.title_or_id() + '</title>'
print '<link href="' + rootUrl + '/stylesheet.css" rel="stylesheet" type="text/css" />'
print '<link rel="icon" href="' + rootUrl + '/other/favicon.ico" type="image/x-icon" />'
print '<link rel="shortcut icon" href="' + rootUrl + '/other/favicon.ico" type="image/x-icon" />'

if string.find(context.REQUEST['HTTP_USER_AGENT'], 'MSIE') < 0:
    print '<script src="http://maps.google.com/maps?file=api&amp;v=2.x&amp;key=' + apiKey + '" type="text/javascript"></script>'

print '<script type="text/javascript" src="javascript.js"></script>'
print '</head>'

print '<body>'

print container.personalBar()
print container.breadcrumbs()

print '<div id="left">'
print container.sitemap()
print container.searchBox()
if not (user.has_role(['Manager'], container) or hasattr(ROOT.people, username)):
    print container.loginBox()
print '</div>'

print '<div id="content">'

return printed
