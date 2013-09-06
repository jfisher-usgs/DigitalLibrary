## Script (Python) "index_html"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Links
##
request  = container.REQUEST
REQUEST  = context.REQUEST
RESPONSE = request.RESPONSE

from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()

user = sec_mgr.getUser()
username = user.getUserName()
owner = REQUEST.AUTHENTICATED_USER.getUserName()

access = user.has_role(['Manager', 'chiefs', 'braves'], context)

###

if REQUEST.form.has_key('action') and REQUEST.form['action'] != 'Cancel':
    
    if REQUEST.form['action'] == 'Delete':
        id = REQUEST.form['id']
        context.manage_delObjects(id)
    else:
        namLink = REQUEST.form['namLink']
        
        urlLink = REQUEST.form['urlLink']
        if urlLink[0:4] != 'http': urlLink = 'http://' + urlLink
        
        desLink = REQUEST.form['desLink']
        
        catLink = REQUEST.form['select_catLink']
        if catLink == '': catLink = REQUEST.form['catLink']
           
        if namLink == '' or urlLink == '' or catLink == '':
            raise Exception, 'incomplete_form'
            
    if REQUEST.form['action'] == 'Add':
        
        id = context.randomId()
        
        context.manage_addFile(id, title=namLink, precondition="", content_type="") 
        
        obj = getattr(context, id)
        
        # Add properties
        obj.manage_addProperty('owner', owner, 'string') 
        obj.manage_addProperty('category', catLink, 'string') 
        obj.manage_addProperty('url', urlLink, 'string')
        obj.manage_addProperty('description', desLink, 'text')
        
        # Change properties
        obj.manage_changeProperties({'title' : namLink})
        
    if REQUEST.form['action'] == 'Save': 
        id = REQUEST.form['id']
        obj = getattr(context, id)
        
        # Change properties
        obj.manage_changeProperties({'title' : namLink})
        obj.manage_changeProperties({'category' : catLink}) 
        obj.manage_changeProperties({'url' : urlLink})
        obj.manage_changeProperties({'description' : desLink})


##########################################################################


print context.standard_html_header(context, request)

print '<h1>Links</h1>'

print '<form action="" method="post" enctype="multipart/form-data">'

items = context.filterObjectValues(['File'])
items = sequence.sort(items, (('category', 'nocase', 'asc'),))

catUnique = []
for item in items:
    cat = item.getProperty('category')
    if cat not in catUnique: catUnique.append(cat)
    
if catUnique != []:
    old = ''
    for item in items:
       new = item.getProperty('category')
       if new != old:
           if old != '': 
               print '</ul>'
               
           print '<h2>' + new + '</h2>'
           old = new
           
           print '<ul class="bullet">' 
           
       id  = item.getId()
       nam = item.getProperty('title')
       des = item.getProperty('description')
       
       url = item.getProperty('url')
       
       print '<li><a href="' + url + '">' + nam + '</a>: '
       print des
       if user.has_role(['Manager', 'chiefs', 'braves'], item):
           print '<button class="iconsSys editButton" type="submit" name="manageLink:action" value="' + id + '" title="Edit link"></button>'
       print '</li>'
       
    print '</ul>'
    
if access:
    print '<p>'
    print '<input type="hidden" name="catUnique" value="' + string.join(catUnique, ";") + '" />'
    print '<input type="submit" name="manageLink:action" value="Add Link" />'
    print '</p>'
    

print '</form>'

print context.standard_html_footer(context, request)

return printed
