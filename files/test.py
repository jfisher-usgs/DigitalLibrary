## Script (Python) "test"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request  = container.REQUEST

ROOT = container.root()
rootUrl = ROOT.absolute_url()

msg = 'Dogs in and out of spaces that are to small for animals of a different bread, such as squirels and other rodets of another bread of small creature or big, depending on how you look at it.'

objName = 'README.txt'
address = 'https://eng.ucmerced.edu/people/jfisher/files/Test/README.txt'
typ = 'text/plain'
iconTyp = 'txtIcon'






print context.standard_html_header(context, request)

print '<h1>Metadata</h1>'

print '<div id="gallery">'

print '<form id="two" action="..." method="post">'



print '<fieldset>'
print '<ol style="padding:1em 1em 0 0;">'
print '<li>'
print '<a href="' + address + '" >' + objName + '</a> '
print '(' + typ + ')</li>'
print '<li>' + address + '</li>'
print '<li>Submitted by Jason Fisher on 2008-08-30</li>'
print '</ol>'
print '</fieldset>'



print '<b class="switch">'
print '<h3><span class="turn_on"><span class="iconsSys collapsedIcon"></span></span><span class="turn_off"><span class="iconsSys expandedIcon"></span></span>Title</h3>'
print '</b>'
print '<div class="hide">'
print '<fieldset>'
print '<ol>'
print '<li>'
print '<label for="label1">Label</label>'
print '<input name="label1" id="label1" class="text" type="text" />'
print '<span class="iconsSys helpIcon" title="' + msg + '" ></span>'
print '</li>'
print '<li>'
print '<label for="label2">Label</label>'
print '<input name="label2" id="label2" class="text" type="text" />'
print '<span class="iconsSys helpIcon" title="' + msg + '" ></span>'
print '</li>'
print '<li>'
print '<label for="label5">Label</label>'
print '<select name="label5" id="label5">'
print '<option>One</option>'
print '<option>Two</option>'
print '<option>Three</option>'
print '</select>'
print '<select name="label6" id="label6">'
print '<option>One</option>'
print '<option>Two</option>'
print '<option>Three</option>'
print '</select>'
print '<span class="iconsSys helpIcon" title="' + msg + '" ></span>'
print '</li>'
print '</ol>'
print '</fieldset>'
print '</div>'



print '<b class="switch">'
print '<h3><span class="turn_on"><span class="iconsSys collapsedIcon"></span></span><span class="turn_off"><span class="iconsSys expandedIcon"></span></span>Title</h3>'
print '</b>'
print '<div class="hide">'
print '<fieldset>'
print '<ol>'
print '<li>'
print '<label for="label3">Label</label>'
print '<textarea rows="5" cols="30"></textarea>'
print '<span class="iconsSys helpIcon" title="' + msg + '" ></span>'
print '</li>'
print '<li>'
print '<label for="label4">Label</label>'
print '<input name="label4" id="label4" class="text" type="text" />'
print '<span class="iconsSys helpIcon" title="' + msg + '" ></span>'
print '</li>'
print '</ol>'
print '</fieldset>'
print '</div>'



print '<fieldset class="submit">'
print '<input type="submit" name="action" value="Save Changes" />'
print '<input type="reset" name="action" value="Cancel" />'
print '<input type="reset" value="Reset" />'
print '<input type="submit" name="metaExport:action" value="Export" />'
print '</fieldset>'



print '</form>'

print '</div>'

print context.standard_html_footer(context, request)

return printed
