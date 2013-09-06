## Script (Python) "filterObjectValues"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=values=None
##title=
##
from ZTUtils import LazyFilter
from AccessControl import getSecurityManager
checkPermission=getSecurityManager().checkPermission
items = []
raw_items = context.objectValues(values)
secure_items = LazyFilter(raw_items, skip='')
for item in secure_items:
    if checkPermission('Access contents information', item):
        items.append(item)
return items
