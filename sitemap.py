## Script (Python) "sitemap"
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

items = sequence.sort(container.filterObjectValues(['Folder']), (('title_or_id', 'nocase', 'asc'),))

print '<div id="navcontainer">'
print '<dl id="navlist">'

print '<dt><a href="' + rootUrl + '" id="current">Home</a></dt>'

for item in items:

    if item.hasProperty('map') and item.getProperty('map') == 1:

        url = item.absolute_url(0)
        print '<dt><a href="' + url + '">' + item.title_or_id() + '</a></dt>'

print '</dl>'
print '</div>'

return printed
