## Script (Python) "imageGallery"
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

from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()

print context.standard_html_header(context, request)

print '<h1>' + context.title + '</h1>'
print '<p></p>'

print '<table>'

print '<tr><td align="left" style="width:1%;">'
if REQUEST.has_key('returnURL'):
    print '<a href="' + REQUEST.returnURL + '" title="Return">'
    print '<span class="iconsSys backOnePage"></span>'
    print '</a>'
else:
    print '<a href="' + REQUEST['URL1'] + '" title="Folder up">'
    print '<span class="iconsSys folderUp"></span>'
    print '</a>'
print '</td>'

print '<td align="left" style="width:98%;">'
print 'The image thumbnails (shown below) provide a link to the original image.'
if context.hasProperty('description'):
    print context.getProperty('description') + '<br />'
print '</td></tr>'

print '</table>'
print '<p></p>'

print '<table width="80%" border="0" align="center" cellspacing="0" cellpadding="5">'

tmp = context.objectValues(['Photo'])
tmp = sequence.sort(tmp, (('id', 'cmp', 'asc'),))

num = 0
items = []
for i in range(len(context.objectIds(['Photo']))):
    try:
        items = items + [tmp[i]]
        num = num + 1
    except:
        pass

for i in range(math.ceil(num / 4.0)):
    print '<tr>'

    lower = i * 4
    upper = lower + 4
    if upper > num: upper = num

    for j in range(lower, upper):
        item = items[j]
        print '<td align="center">'
        print '<div class="thumbnail">'
        print '<a href="' + item.absolute_url(0) + '/imageView">'
        print item.tag(display="thumbnail", cookie=0, css_class=None, title=item.title_or_id())
        print '</a></div></td>'

    print '</tr>'

print '</table>'

print context.standard_html_footer(context, request)

return printed
