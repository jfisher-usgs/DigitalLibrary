## Script (Python) "registration"
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

ROOT = container.root()
rootUrl = ROOT.absolute_url()

print context.standard_html_header(context, request)

print '<form onsubmit="return checkRegForm();" method="post" action="' + rootUrl + '/people/initialize">'

print '<fieldset>'

print '<h1>Registration</h1>'
print 'Only register if you have been invited to do so by a site member. Permissions are activated by a site manager after registration has been submitted.'

print '<ol>'

print '<li>'
print '<label for="email">Email Address <span class="comment">(this is your User Name)</span></label>'
print '<input type="text" value="" name="email" id="email" size="30" />'
print '<div class="error" id="emailError">Required: Please enter a valid email address</div>'
print '</li>'

print '<li>'
print '<label for="fname">First&nbsp;Name</label>'
print '<input type="text" value="" name="fname" id="fname" size="30" />'
print '<div class="error" id="fnameError">Required: Please enter your first name</div>'
print '</li>'

print '<li>'
print '<label for="mname">Middle&nbsp;Initial</label>'
print '<input type="text" value="" name="mname" id="mname" size="30" />'
print '</li>'

print '<li>'
print '<label for="lname">Last&nbsp;Name</label>'
print '<input type="text" value="" name="lname" id="lname" size="30" />'
print '<div class="error" id="lnameError">Required: Please enter your last name</div>'
print '</li>'

print '<li>'
print '<label for="website url">Website</label>'
print '<span class="genuine"><input type="text" value="" name="website" id="website" size="30" /></span>'
print '<input type="text" value="" name="url" id="url" size="30" />'
print '<div class="error" id="lnameError">Required: Please enter your last name</div>'
print '</li>'

print '<li>'
print '<label for="notes">Comment <span class="comment">(e.g. source of invitation, groups you&#39;d like to join)</span></label>'
print '<textarea name="notes" id="notes" rows="4" cols="60"></textarea>'
print '</li>'

print '</ol>'
print '</fieldset>'

print '<fieldset class="submit">'
print '<input type="submit" name="action" value="Register" />'
print '</fieldset>'

print '</form>'

print '<script type="text/javascript">setDefaultFocus(\'email\');</script>'

print context.standard_html_footer(context, request)

return printed
