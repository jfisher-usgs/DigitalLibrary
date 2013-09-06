## Script (Python) "form_batchUpload"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=numFiles=12
##title=
##
request  = container.REQUEST
REQUEST  = context.REQUEST

publicStatus = ''
if not context.anonymousHasPermission(context):
    publicStatus = 'DISABLED'

print context.standard_html_header(context, request)

print '<h1>Batch Upload</h1>'

print '<form action="' + REQUEST['URL1'] + '" method="post" enctype="multipart/form-data" name="objectUploads">'

print '<table width="100%" cellspacing="0" cellpadding="2" border="0">'

print '<tr><th style="width:1%;"></th><th style="width:99%;"></th></tr>'

for i in range(numFiles):
    print '<tr>'
    print '<td style="padding-top:0.25em;">'
    print '<input type="checkbox" name="public:list" id="publicList" value="file.name' + str(i) + '" title="Grant anonymous users view/access permissions" ' + publicStatus + ' />'
    print '</td>'
    print '<td><input type="file" name="file.name' + str(i) + '" size="40" /></td>'
    print '</tr>'
    
print '<tr>'
print '<td style="padding-top:0.5em;">'
print '<input type="checkbox" id="theController" name="theController" title="Select/unselect all" onclick="toggleSelect(\'objectUploads\', \'theController\', \'publicList\')" />'
print '</td>'
print '<td style="padding-top:0.5em;">'
print '<input type="submit" name="action" value="Upload" />'
print '<input type="submit" name="action" value="Cancel" />'
print '</td>'
print '</tr>'

print '</table>'

print '</form>'

print context.standard_html_footer(context,request)

return printed
