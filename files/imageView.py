## Script (Python) "imageView"
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

print context.standard_html_header(context, request)

print '<p></p>'

path = context.absolute_url(0) + '/imageView'
numDis = str(len(context.displayIds()))

print '<div class="pagination">'
try:
    print '<a href="' + context.prevPhoto().absolute_url(0) + '/imageView" style="font-family: arial;">&#9668;</a>'
except:
    print '<span class="disabled" style="font-family: arial;">&#9668;</span>'

print '<a href="' + REQUEST['URL2'] + '/imageGallery">Back to Gallery</a>'

try:
    print '<a href="' + context.nextPhoto().absolute_url(0) + '/imageView" style="font-family: arial;">&#9658;</a>'
except:
    print '<span class="disabled" style="font-family: arial;">&#9658;</span>'
print '</div>'

display = REQUEST.get('display', 'medium')

print '<table border="0" cellpadding="0" cellspacing="0" width="75%" align="center">'
print '<tr><td align="center" colspan="' + numDis + '">'
print context.tag(display=display, border=1, cookie=1, alt='', title='')
print '</td></tr>'
print '</table>'

print '<div class="pagination">'
for i in context.displayIds():  
    if i == display:
        print '<span class="current">' + i + '</span>' 
    else:
        print '<a href="' + path + '?display=' + i + '">' + i + '</a>' 
print '</div>'

print '<div class="pagination">'
print '<a href="' + context.absolute_url(0) + '?display=">Download highest resolution</a>'
print '</div>'

print context.standard_html_footer(context, request)

return printed
