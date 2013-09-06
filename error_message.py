## Script (Python) "error_message"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=error_type, error_message, error_tb, error_value
##title=
##
request  = container.REQUEST

print context.standard_html_header(context, request)

if error_type == 'NotFound':
    print error_message
    return printed

print '<h1>Site Error</h1>'
print '<p></p>'
print 'An error was encountered while publishing this resource.'

print '<h2>Type</h2>'
print error_type

print '<h2>Message</h2>'
print error_message

print '<h2>Traceback</h2>'
print error_tb

print '<h2>Value</h2>'
print error_value


print '<p></p>'
print '<p>If the error persists please contact the site maintainer. Thank you for your patience.</p>'

print context.standard_html_footer(context, request)

return printed
