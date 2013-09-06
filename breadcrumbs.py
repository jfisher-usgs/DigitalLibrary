## Script (Python) "breadcrumbs"
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

ROOT = container.root()

breadcrumbs = None

for crumb in PARENTS:
    if crumb == ROOT: 
        breadcrumbs = ['<a href="' + ROOT.absolute_url() + '">Home</a>']
    elif breadcrumbs:
        
        display = ''
        if crumb.meta_type == 'Photo': display = '?display='
        
        breadcrumbs += ['<a href="' + crumb.absolute_url() + display + '">' + crumb.title_or_id() + '</a>']
        
print '<div id="breadcrumbs">'
print string.join(breadcrumbs, "&nbsp;<strong>&raquo;</strong>&nbsp;")
print '</div>'

return printed
