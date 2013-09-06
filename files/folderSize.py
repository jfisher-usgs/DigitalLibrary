## Script (Python) "folderSize"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj, typs
##title=
##
from DateTime import DateTime

def checkSize(id, obj, lst=None, detail=0):
    if lst is None: lst = []

    content_size = 0
    folders = []
    for i, o in obj.objectItems(typs):
        if o.isPrincipiaFolderish:
            folders.append((i, o))
        else:
            if hasattr(o, 'get_size'):
                try:
                    size = o.get_size()
                    lst.append((i, size))
                    content_size = content_size + size
                except:
                    lst.append(('ERROR: %s' % i, 0))

    for i, o in folders:
        ret = checkSize('%s/%s' % (id, i), o, lst, detail)
        content_size = content_size + ret[0]

    return (content_size, lst)

###

val = {}

for i, o in obj.objectItems(typs):
    if o.isPrincipiaFolderish:
        s = checkSize(i, o)
        val[i] = s[0]

return val
