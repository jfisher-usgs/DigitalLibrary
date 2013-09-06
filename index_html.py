## Script (Python) "index_html"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Home
##
request  = container.REQUEST

ROOT = container.root()

print context.standard_html_header(context, request)

print '<h1>Jason C. Fisher</h1>'

print '<h5>Welcome to my thread in the world wide web...</h5>'

print '''
<p>Contained within these pages is information about myself and those tools which I use 
to perform my art, an art form which can only be described as a blend of geohydrology, 
computer science, and graphic design. To students of these disciplines, may the information 
within these pages help you along your way. If you have any comments or questions 
regarding any aspect of this site, please send them to '''

print context.antispam(ROOT.getProperty('email'), mailTo=True) + '.</p>'

print '<p>'
print '<a href="./files/Photos/Environment/tower_lake.jpg/imageView">'
print '<img src="./other/jfisher.jpg" class="logo" width="266" height="200" alt="Tower Lake" />'
print '</a>'
print '</p>'

print '<p>"Hills cherish the ambition to turn into partial differential equations."'
print '<a href="./other/perfect_life">Donald&nbsp;Hall</a></p>'

print context.standard_html_footer(context, request)

return printed
