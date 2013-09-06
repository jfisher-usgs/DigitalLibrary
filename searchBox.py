## Script (Python) "searchBox"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
ROOT = container.root()
rootUrl = ROOT.absolute_url()

print '<form action="' + rootUrl + '/catalog/index_html">'

print '<div class="box">'

print '<h5>Search</h5>'

print '<div class="content">'

print '<input type="text" name="q" /><br />'

print '<input type="submit" value="Search" />&nbsp;'

print '<a href="' + rootUrl + '/catalog/index_html?type=Advanced">Advanced</a>'

print '</div></div></form>'

return printed
