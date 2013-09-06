## Script (Python) "initialize"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=email=None, fname=None, lname=None, mname=None, url=None, website=None, notes=None
##title=
##

ROOT = container.root()

# check the validity of the incoming parameters
if not email:
    raise Exception, 'incomplete_form'
if not fname:
    raise Exception, 'incomplete_form'
if not lname:
    raise Exception, 'incomplete_form'
if website:
    raise Exception, 'post_rejected'

# check to see whether email is in use
if len(container.people.catalog(id=email)) > 0:
    raise Exception, 'email_in_use'

# import random python scripts
from Products.PythonScripts.standard import url_quote

# create a temporary password and secret.
password = str(random.randrange(100000, 999999))
secret   = str(random.randrange(100000, 999999))

# set up a REQUEST in order to make a user
REQUEST = {}
REQUEST['name'] = email
REQUEST['roles'] = None
REQUEST['password'] = password
REQUEST['confirm']  = password

# make a acl_user object
RESPONSE = {}
container.acl_users.Users.acl_users.manage_users('Add', REQUEST, RESPONSE)

# make a user folder object
if mname:
    fullName = "%s, %s %s" % (lname, fname, mname)
else:
    fullName = "%s, %s" % (lname, fname)

container.people.manage_addFolder(email, fullName)

# add the local role and properties to the user's folder
person = container.people[email]

person.manage_permission(permission_to_manage='Manage properties', roles=['Manager', 'Owner', 'chiefs'])

date = person.bobobase_modification_time()
timeZone = ROOT.getProperty('timeZone')

person.manage_setLocalRoles(email, ('Owner', ))

person.manage_addProperty('name_first', fname, 'string')
person.manage_addProperty('name_middle', mname, 'string')
person.manage_addProperty('name_last', lname, 'string')
person.manage_addProperty('secret', secret, 'string')
person.manage_addProperty('registered', date, 'date')
person.manage_addProperty('url', url, 'string')
person.manage_addProperty('organization', '', 'string')
person.manage_addProperty('interests', '', 'text')
person.manage_addProperty('public', 0, 'boolean')
person.manage_addProperty('groups', '', 'lines')
person.manage_addProperty('role', 'New Member', 'string')
person.manage_addProperty('manageGroups', '', 'lines')
person.manage_addProperty('timeZone', timeZone, 'string')

# catalog information pertaining to the user folder
container.people.catalog.catalog_object(person)

# create url for calling the password_set() python script, include both the user id and secret within the URL.
passurl = '%s?id=%s&secret=%s' %(container.people.password.absolute_url(), url_quote(email), secret)

# initialize comments
comments = ''
if notes:
    comments = str(notes)

# contact the site Managers with the new members information

rcp = [ROOT.getProperty('email')]

for result in container.catalog({'role' : 'Manager'}):
    if result.id not in rcp:
        rcp += [result.id]

msg =  'The following user information has been submitted for site registration.\n\n'
msg += 'New Member: ' + fullName + '\nEmail Address: ' + email + '\nWebsite: ' + url + '\nComments: ' + comments
msg += '\n\nIf you know the individual and wish to upgrade their permissions, please do so.\n\n'
msg += 'Questions, contact the site administrator at '
msg += ROOT.getProperty('email') + '\n'

container.sendMail(recipients=rcp, sender=email, subject='New Member', message=msg)

# direct user to password form
context.REQUEST.response.redirect(passurl)

return(email)
