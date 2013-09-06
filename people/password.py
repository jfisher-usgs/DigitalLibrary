## Script (Python) "password"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id=None, secret=None, confirm=None, password=None, email=None
##title=
##
# import a standard function, and get the HTML request and response objects.
from Products.PythonScripts.standard import html_quote, url_quote
import string

ROOT = container.root()

request  = container.REQUEST
REQUEST  = context.REQUEST
RESPONSE = request.RESPONSE

print context.standard_html_header(context, request)

###

if (id and secret and secret == container.people[id].getProperty('secret')):
    person = container.people[id]
    
    if password is None or password != confirm:
        if password != confirm:
            raise Exception, 'password_confirmation_mismatch'
            
        fname = person.getProperty('name_first')
        mname = person.getProperty('name_middle')
        lname = person.getProperty('name_last')
        if mname == '': user = fname + ' ' + lname
        else: user = fname + ' ' + mname + ' ' + lname
        
        print '<form onSubmit="return checkPwdForm();" method="post" action="">'
        
        print '<input type="hidden" name="id" id="id" value="' + id + '" />'
        print '<input type="hidden" name="secret" value="' + secret + '" />'
        
        print '<fieldset>'
        print '<h1>Password</h1>'
        print 'Please set the password for <b>' + user + '</b>. The user name (login) for this account is <b>' + person.getId() + '</b>.'
        print 'You will need to login with this user name and the password given below in order to use this account.'
        print '<ol>'
        
        print '<li>'
        print '<label for="password">Password</label>'
        print '<input type="password" value="" name="password" id="password" size="30" />'
        print '</li>'
        
        print '<li>'
        print '<label for="confirm">Confirmation <span class="comment">(enter password again)</span></label>'
        print '<input type="password" value="" name="confirm" id="confirm" size="30" />'
        print '<span class="error" style="display:block;" id="msg"> </span>'
        print '</li>'
        
        print '</ol>'
        print '</fieldset>'
        
        print '<fieldset class="submit">'
        print '<input type="submit" name="action" value="Set Password" />'
        print '</fieldset>'
        
        print '</form>'
        
        print '<script type="text/javascript">setDefaultFocus(\'password\');</script>'
        
    else:
        REQ = {}
        REQ['name']     = person.getId()
        REQ['password'] = password
        REQ['confirm']  = password
        REQ['domains']  = None
        REQ['roles']    = container.acl_users.Users.acl_users.getUser(person.getId()).getRoles()
        REQ['submit']   = 'Change'
        container.acl_users.Users.acl_users.manage_users(submit='Change', REQUEST=REQ)
        
        person.manage_delProperties(('secret',))
        
        context.REQUEST.RESPONSE.setCookie('__ac_name', person.getId())
        context.REQUEST.RESPONSE.setCookie('__ac_password', password)
        
        logurl = '%s/login?action=' %(container.absolute_url())
        context.REQUEST.response.redirect(logurl)

###

elif email:
    results = container.people.catalog(id=email)
    results_count = len(results)
    
    if results_count == 0:
        print '<h1>Error</h1>'
        print '<p>The user name ' + email + ' is not associated with any of the users we have on record. '
        
        manEmail = ROOT.getProperty('email')
        print 'Please contact the site monitor at '
        print context.antispam(manEmail) + '.'
        print '</p>'
        
    elif results_count == 1:
        person = results[0].getObject()
        userid = person.getId()
        
        secret = str(random.randrange(100000, 999999))
        
        if person.hasProperty('secret'):
            person.manage_delProperties(('secret',))
        
        person.manage_addProperty('secret', secret, 'string')
        secret = person.getProperty('secret')
        
        passurl = '%s?id=%s&secret=%s' %(script.absolute_url(), url_quote(userid), secret)
        
        rcp = person.getId()
        snd = ROOT.getProperty('email')
        sbj = 'Password Reset Instructions'
        msg = '\nA password reset was requested for your account. To continue, please go to the URL below.\n' + passurl + '\n'
        
        container.sendMail(recipient=rcp, sender=snd, subject=sbj, message=msg)
        
        print '<h1>Password Instructions</h1>'
        print '<p>Instructions for password reset have been sent to ' + person.getId() + '.</p>'

###

else:
    
    
    print '<form method="get" action="">'
    
    print '<fieldset>'
    
    print '<h1>Reset Password</h1>'
    print 'In order to reset your password, you must provide the email address that is on file for you. '
    print 'Instructions for resetting your password will be sent to this address.'
    print '<ol>'
    
    print '<li>'
    print '<label for="email">Email Address</label>'
    print '<input type="text" value="" name="email" id="email" size="30" />'
    print '</li>'
    
    print '</ol>'
    print '</fieldset>'
    
    print '<fieldset class="submit">'
    print '<input type="submit" name="action" value="Send Instructions" />'
    print '</fieldset>'
    
    print '</form>'
    
    print '<script type="text/javascript">setDefaultFocus(\'email\');</script>'
    
print context.standard_html_footer(context, request)

return printed
