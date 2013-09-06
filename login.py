## Script (Python) "login"
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
RESPONSE = request.RESPONSE

from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()

user = sec_mgr.getUser()
username = user.getUserName()

ROOT = container.root()
rootUrl = ROOT.absolute_url()

if REQUEST.has_key('came_from'):
    came_from = REQUEST.came_from
else:
    came_from = rootUrl

members = context.people.catalog.uniqueValuesFor('id')

print context.standard_html_header(context,request)

if REQUEST.form.has_key('action'):
    if username == 'Anonymous User':
        print '<h1>Login Failure</h1>'
        print '<p>You are not currently logged in. Your user name and/or password may be incorrect.</p>'
    elif username not in members and not user.has_role(['Manager'], container):
        RESPONSE.expireCookie('__ac', path='/')
        print '<h1>Login Failure</h1>'
        print '<p>Your username is not included in the list of site users.  This error is typically due to cookie conflicts on your browser.  To remedy the situation erase all cookies on your browser including Authenticated Sessions in Firefox.</p>'
    else:
        RESPONSE.redirect(came_from)
else:
    print '<form method="post" action="">'
    
    print '<fieldset>'
    
    print '<h1>Please Login</h1>'
    print 'If you do not have an account here, head over to the' 
    print '<a href="' + rootUrl + '/people/registration">registration form</a> to become a member.'
    
    print '<ol>'
    
    print '<li>'
    print '<label for="__ac_name">User Name <span class="comment">(email address)</span></label>'
    print '<input type="text" name="__ac_name" id="__ac_name" size="30" />'
    print '</li>'
    
    print '<li>'
    print '<label for="__ac_password">Password</label>'
    print '<input type="password" name="__ac_password" id="__ac_password" size="30" />'
    print '</li>'
    
    print '</ol>'
    print '</fieldset>'
    
    print '<fieldset class="submit">'
    print '<input type="submit" name="action" value=" Login " />'
    
    print '<ol>'
    
    print '<li>'
    print '<label class="noform">Forgotten your password?</label>'
    print 'Click <a href="' + rootUrl + '/people/password">here</a> to reset your password.'
    print '</li>'
    
    print '<li>'
    print '<label class="noform">Having trouble logging in?</label>'
    print 'Make sure to <a href="http://www.google.com/cookies.html">enable cookies</a> in your web browser.'
    print '</li>'
    
    print '</ol>'
    
    print '</fieldset>'
    
    print '</form>'

print context.standard_html_footer(context,request)

return printed
