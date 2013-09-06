## Script (Python) "fileSize"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=bytes
##title=
##
"""
Return a string describing the size of a file.
"""

bytes = int(bytes)

if bytes == 0: return "0 KB"

kb = bytes/1024.0
mb = bytes/1048576.0
gb = bytes/1073741824.0

if gb > 1:
    return "%.2f GB" % gb
elif mb > 1:
    return "%.2f MB" % mb
elif kb > 1:
    return "%d KB" % kb

return "1 KB"
