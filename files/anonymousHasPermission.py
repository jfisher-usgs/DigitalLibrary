## Script (Python) "anonymousHasPermission"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=item, permission='View'
##title=
##

# This script needs the "Manager" proxy role to work for all users.

ps = item.permission_settings()
acquired = False
for p in ps:
    if p['name'] == permission:
        acquired = not not p['acquire']
        break
if acquired: 
    parent = item.aq_parent
    return context.anonymousHasPermission(parent, permission)
else:
    for p in item.rolesOfPermission(permission):
        if p['name'] == "Anonymous":
            selected = not not p['selected']
            return selected
