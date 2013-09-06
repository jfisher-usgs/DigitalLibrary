## Script (Python) "loginBox"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
PARENTS = context.REQUEST.PARENTS
PARENTS.reverse()
parent = PARENTS[0]

ROOT = container.root()
rootUrl = ROOT.absolute_url()

print '<form action="' + rootUrl + '/login" id="login_box_form" method="post">'

print '<div class="box">'

print '<h5>Login</h5>'

print '<div class="content">'

print '<strong>User Name</strong><br />'
print '<input type="text" name="__ac_name" /><br />'

print '<strong>Password</strong><br />'
print '<input type="password" name="__ac_password" /><br />'
print '<input type="submit" name="action" value="Login" /><br />'

print '<input type="hidden" name="came_from" value="' + parent.absolute_url() + '" />'

print '<a href="' + rootUrl + '/people/password">Forgot Password</a><br />'
print '<a href="' + rootUrl + '/people/registration">New User</a>'

print '</div></div></form>'

return printed
