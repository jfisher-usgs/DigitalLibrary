## Script (Python) "form_metadata"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
import DateTime

request  = container.REQUEST
REQUEST  = context.REQUEST
RESPONSE = request.RESPONSE

ROOT = container.root()
rootUrl = ROOT.absolute_url()

indexes = container.catalog.indexes()

from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()
user = sec_mgr.getUser()

username = user.getUserName()
userobj = getattr(container.people, username, None)
if userobj is not None and userobj.hasProperty('timeZone'):
    timeZone = userobj.getProperty('timeZone')
else:
    timeZone = ROOT.getProperty('timeZone')

# format value in filed (character string) format
def valFmt(val, type):
    if type == 'lines':
        val = string.join(val, "; ")
    elif type == 'tokens': 
        val = string.join(val, " ")
    elif type == 'date' and val != '':
        val = val.strftime('%x') + ' ' + val.strftime('%X')
    elif type == 'float' or type == 'int':
        val = str(val)
    val = string.strip(val)
    return val

id = REQUEST.form['form_metadata']

obj = getattr(context, id)

fileroot = rootUrl + '/files'

access = user.has_role(['Owner', 'Manager'], obj)

meta_title    = container.files.getProperty('metaTitle')
meta_types    = container.files.getProperty('metaTypes')
meta_category = container.files.getProperty('metaCategory')

catUnique = []
for i in meta_category:
    if i not in catUnique:
        catUnique.append(i)
        
meta_items = []
for i in meta_title:
    meta_items = meta_items + [container.string2id(i)]
    
meta_value = []

objName = obj.title_or_id()
address = obj.absolute_url(0)

if obj.meta_type == 'Photo': 
    typ = obj.content_type()
else:
    typ = obj.getProperty('content_type')

urlExt = None
if obj.hasProperty('urlExternalLink'):
    urlExt = obj.getProperty('urlExternalLink')
    
submitBy = None
if obj.hasProperty('submitted_by'):
    hld = obj.getProperty('submitted_by')
    hld = getattr(container.people, hld, None)
    if hld and hld.hasProperty('name_first'):
        submitBy = string.join([hld.getProperty('name_first'), hld.getProperty('name_middle'), hld.getProperty('name_last')], ' ')
        if hld.getProperty('public') or access:
            submitBy = '<a href="' + hld.absolute_url() + '?back=1">' + submitBy + '</a>'
        
submitOn = None
if obj.hasProperty('submitted_on'):
    dt = obj.getProperty('submitted_on')
    dt = dt.toZone(timeZone)
    submitOn = dt.ISO()
    
lastMod = obj.bobobase_modification_time().toZone(timeZone).ISO()

Str = ''
if submitBy or submitOn:
    Str = 'added'
    if submitBy:
        Str += ' by ' + submitBy
    if submitOn:
        Str += ' on ' + submitOn
    Str += ', '
Str += 'last modified on ' + lastMod

#####################

print context.standard_html_header(context, request)

print '<h1>Metadata</h1>'
print '<form action="" method="post">'
print '<input type="hidden" name="obj_id" value="' + id + '" />'

print '<fieldset>'
print '<ol>'
if access:
    print '<li>' + objName + ' (' + typ + ')</li>'
    print '<li><a href="' + address + '" >' + address + '</a></li>'
    print '<li>' + Str + '</li>'
    if urlExt:
        print '<li>'
        print '<label for="urlExternalLink">External URL</label>'
        print '<input type="text" style="width:30em;" name="urlExternalLink" id="urlExternalLink" value="' + urlExt + '" />'
        print '</li>'
else:
    print '<li><label class="noform">Name:</label>' + objName + '</li>'
    print '<li><label class="noform">Type:</label>' + typ + '</li>'
    print '<li><label class="noform">URL:</label><a href="' + address + '">' + address + '</a></li>'
    if submitBy:
        print '<li><label class="noform">Added by:</label>' + submitBy + '</li>'
    if submitOn:
        print '<li><label class="noform">Added on:</label>' + submitOn + '</li>'
    print '<li><label class="noform">Last modified on:</label>' + lastMod + '</li>'
    if urlExt:
        print '<li><label class="noform">External URL:</label><a href="' + urlExt + '">' + urlExt + '</a></li>'
print '</ol>'
print '</fieldset>'

if access:
    print '<div id="gallery">'

for i in catUnique:
    addHeader = True
    for j in range(len(meta_items)):
        if meta_category[j] == i:
            
            itm = meta_items[j]
            typ = meta_types[j]
            tit = meta_title[j]
            
            print '<input type="hidden" name="meta_items:list" value="' + itm + '" />'
            print '<input type="hidden" name="meta_types:list" value="' + typ + '" />'
            print '<input type="hidden" name="meta_title:list" value="' + tit + '" />'
            
            valParent = ''
            cssParent = ''
            
            parent = obj.aq_parent
            while parent.absolute_url() != fileroot and valParent == '':
                if parent.hasProperty(itm):
                    valParent = parent.getProperty(itm)
                parent = parent.aq_parent
            print '<input type="hidden" name="valParent:list" value="' + valFmt(valParent, typ) + '" />'
            
            if obj.hasProperty(itm):
                val = obj.getProperty(itm)
            else:
                val = valParent 
                if valParent != '':
                    cssParent = 'id="inherited"'
            val = valFmt(val, typ)
            print '<input type="hidden" name="meta_value:list" value="' + val + '" />'
            
            if access:
                if addHeader:
                    print '<b class="switch">'
                    print '<h3><span class="turn_on"><span class="iconsSys collapsedIcon"></span></span><span class="turn_off"><span class="iconsSys expandedIcon"></span></span>' + i + '</h3>'
                    print '</b>'
                    print '<div class="hide">'
                    print '<fieldset>'
                    print '<ol>'
                    
                print '<li>'
                print '<label for="' + itm + '">' + tit + '</label>'
                
                if typ == 'text':
                    print '<textarea ' + cssParent + ' rows="4" style="width:30em;" name="' + itm + '">' + val + '</textarea>'
                elif typ == 'lines':
                    print '<input ' + cssParent + ' type="text" style="width:30em;" name="' + itm + '" value="' + val + '" />'
                elif typ == 'date':
                    print container.dateTime(itm, val, cssParent=cssParent)
                else:
                    if typ in ['float', 'int']:
                        print '<input ' + cssParent + ' type="text" style="width:10em;"  name="' + itm + '" value="' + str(val) + '" />'
                    else:
                        print '<input ' + cssParent + ' type="text" style="width:30em;" name="' + itm + '" value="' + str(val) + '" />'
                        
                print '<span class="iconsSys helpIcon" title="' + container.help(key="Metadata", typ=typ) + '" ></span>'
                
                if typ == 'lines':
                    if val == '': val = []
                    else: val = string.split(val, "; ")
                    if itm in indexes:
                        catVals = container.catalog.uniqueValuesFor(itm)
                        if catVals:
                            flag = False
                            for k in catVals:
                                if k not in val: 
                                    if not flag: 
                                        flag = True
                                        print '<br /><select style="width:15em;margin-top:0.35em;" size="3" name="select_' + itm + ':list"  multiple>'
                                    print '<option>' + k + '</option>'
                            if flag: print '</select>'
                            
                print '</li>'
                
            elif val != '':
                if addHeader:
                    print '<fieldset>'
                    print '<h3>' + i + '</h3>'
                    print '<ol>'
                print '<li><label class="noform">' + tit + ':</label>' + val + '</li>'
                
            addHeader = False
            
    print '</ol>'
    print '</fieldset>'
    if access:
        print '</div>'

print '<fieldset class="submit">'
if access: 
    print '<input type="submit" name="action" value="Save Changes" />'
    print '<input type="submit" name="action" value="Cancel" />'
    print '<input type="reset" value="Reset" />'
else:
    print '<input type="submit" name="action" value="Return" />'
print '<input type="submit" name="metaExport:action" value="Export" />'
print '</fieldset>'

print '</form>'

if access:
    print '</div>'

print '<script type="text/javascript">toggleForm();</script>'

print context.standard_html_footer(context,request)

return printed
