## Script (Python) "index_html"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Files
##
from Products.PythonScripts.standard import html_quote
import DateTime

request  = container.REQUEST
REQUEST  = context.REQUEST
RESPONSE = request.RESPONSE
session  = request.SESSION

if context.hasProperty('urlExternalLink'):
    RESPONSE.redirect(context.getProperty('urlExternalLink'))

ROOT = container.root()
rootUrl = ROOT.absolute_url()

indexes = container.catalog.indexes()

if REQUEST.has_key('returnURL'):
    RESPONSE.expireCookie('returnURL')

# Object Id Can Not be Identical to ZCatalog Index (lame)
def indexCheck(id):
    while id in indexes:
        id = id + '_'
    return id

# Delete All ZCatalog Indexes Associated with an Object
def delCatObj(objId):
    if not same_type(objId,[]): objId = [objId]
    for i in range(len(objId)): 
        object = getattr(context, objId[i])
        uid = '/'.join(object.getPhysicalPath())
        container.catalog.uncatalog_object(uid)
        if object.meta_type in ['Folder', 'Photo Folder']:
            container.recursiveUpdate(object, catObj=False)

# Add/Update ZCatalog Indexes Associated with an Object
def addCatObj(objId, update_metadata=1, idxs=None, oldVals=None, newVals=None):
    
    if idxs != None:
        idxs = [i for i in idxs if i in indexes]
    
    if not same_type(objId,[]): 
        objId = [objId] 
    for i in range(len(objId)):
        object = getattr(context, objId[i])
        
        container.catalog.catalog_object(object, idxs=idxs, update_metadata=update_metadata)
        if object.meta_type in ['Folder', 'Photo Folder']:
            container.recursiveUpdate(object, catObj=True, update_metadata=update_metadata, idxs=idxs, oldVals=oldVals, newVals=newVals)

##########################################################

from AccessControl import getSecurityManager
sec_mgr = getSecurityManager()

user = sec_mgr.getUser()
username = user.getUserName()

userobj = getattr(container.people, username, None)
if userobj is not None and userobj.hasProperty('timeZone'):
    timeZone = userobj.getProperty('timeZone')
else:
    timeZone = ROOT.getProperty('timeZone')

sysTime = DateTime.DateTime()

access = user.has_role(['Manager', 'chiefs', 'braves'], context)

# Identify Selected Objects
if REQUEST.form.has_key('file'):
    fileId = REQUEST.form['file']

# Delete Selected Objects
if REQUEST.form.has_key('delete') and REQUEST.form.has_key('file'):
    delCatObj(fileId)
    context.manage_delObjects(fileId)

# Cut Selected Objects
if REQUEST.form.has_key('cut') and REQUEST.form.has_key('file'):
    delCatObj(fileId)
    cut_info = context.manage_cutObjects(fileId, )
    session.set('cb', cut_info)

# Copy Selected Objects
if REQUEST.form.has_key('copy') and REQUEST.form.has_key('file'):
    copy_info = context.manage_copyObjects(fileId, )
    session.set('cb', copy_info)

# Paste Objects that are Stored in Memory (from a previous Copy/Cut)
if REQUEST.form.has_key('paste'):
    objs = session.get('cb')
    if objs != None:
        objIds = context.manage_pasteObjects(objs)
        context.image2photo()
        for objId in objIds:
            
            if objId['id'] != objId['new_id']:
                obj = getattr(context, objId['new_id']) 
                hld = 'Copy of ' + obj.getProperty('title')
                obj.manage_changeProperties({'title' : hld})
                
            addCatObj(objId['new_id'], update_metadata=0)

# Process Forms

if REQUEST.form.has_key('action'):
    
  # Identify Objects Contained within Current Folder
    objs = context.objectIds()
    
  # Rename Object
    if REQUEST.form['action'] == 'Rename': 
        oldNames = REQUEST.form['old_name'] 
        newNames = REQUEST.form['new_name'] 
        
        for i in range(len(newNames)): 
            old_name = oldNames[i]
            hld = string.strip(newNames[i])
            new_name = container.string2id(hld)
            new_name = indexCheck(new_name)
            
            obj = getattr(context, old_name)
            
            if new_name == old_name:
                obj.manage_changeProperties({'title' : hld})
            
            if new_name not in objs:
                obj = getattr(context, old_name)
                
                context.manage_renameObject(old_name, new_name, )
                
                object = getattr(context, new_name)
                object.manage_changeProperties({'title' : hld})
                
                addCatObj(new_name, update_metadata=0)
                
                
  # Add New Link
    if REQUEST.form['action'] == ' Add ' and REQUEST.form.has_key('new_link_url'):
        
        if REQUEST.form['new_link_name'] == '' and REQUEST.form['new_link_url'] == '':
            raise Exception, 'incomplete_form'
            
        hld = string.strip(REQUEST.form['new_link_name'])
        newlink = container.string2id(hld)
        newlink = indexCheck(newlink)
        
        if newlink not in objs:
            
            context.manage_addFolder(newlink)
            
            obj = getattr(context, newlink)
            
            # Add properties
            obj.manage_changeProperties({'title' : hld})
            obj.manage_addProperty('content_type', 'external/link', 'string')
            
            url = REQUEST.form['new_link_url']
            if url[0:4] != 'http': url = 'http://' + url
            obj.manage_addProperty('urlExternalLink', url, 'string')
            
            obj.manage_addProperty('submitted_by', username, 'string')
            obj.manage_addProperty('submitted_on', sysTime, 'date')
            
            for usr in context.users_with_local_role('Owner'):
                obj.manage_addLocalRoles(usr, ('Owner',))
            for usr in context.users_with_local_role('Observer'):
                obj.manage_addLocalRoles(usr, ('Observer',))
                
            if REQUEST.form.has_key('public_link'):
                roles = []
                acquire = 1
            else:
                roles = ['Manager', 'Owner', 'chiefs']
                acquire = 0
                
            obj.manage_permission('Access contents information', roles, acquire)
            obj.manage_permission('View', roles, acquire)
            
            context.catalog.catalog_object(obj)
            
            
  # Add New Folder
    if REQUEST.form['action'] == ' Add ' and REQUEST.form.has_key('new_folder'):
        
        if REQUEST.form['new_folder'] == '':
            raise Exception, 'incomplete_form'
            
        hld = string.strip(REQUEST.form['new_folder'])
        newfolder = container.string2id(hld)
        newfolder = indexCheck(newfolder)
        
        if newfolder not in objs:
            
            if REQUEST.form.has_key('image_folder'): 
                context.manage_addProduct['Photo'].manage_addPhotoFolder(newfolder, '')
            else:
                context.manage_addFolder(newfolder)
                
            obj = getattr(context, newfolder)
            
            # Add properties
            obj.manage_changeProperties({'title' : hld})
            
            if REQUEST.form.has_key('image_folder'): 
                obj.manage_addProperty('content_type', 'folder/image', 'string') 
            else:
                obj.manage_addProperty('content_type', 'folder', 'string')
                
            obj.manage_addProperty('submitted_by', username, 'string')
            obj.manage_addProperty('submitted_on', sysTime, 'date')
            
            for usr in context.users_with_local_role('Owner'):
                obj.manage_addLocalRoles(usr, ('Owner',))
            for usr in context.users_with_local_role('Observer'):
                obj.manage_addLocalRoles(usr, ('Observer',))
                
            if REQUEST.form.has_key('public_folder'):
                roles = []
                acquire = 1
            else:
                roles = ['Manager', 'Owner', 'chiefs']
                acquire = 0
                
            obj.manage_permission('Access contents information', roles, acquire)
            obj.manage_permission('View', roles, acquire)
            
            context.catalog.catalog_object(obj)
            
            
  # Upload Files
    if REQUEST.form['action'] == 'Upload':
        
        public = []
        if REQUEST.form.has_key('public'):
            public = REQUEST.form['public']
        
        for key in context.REQUEST.keys():
            if key[:5] == 'file.' and REQUEST[key].filename:
                
                filename = REQUEST[key].filename
                i = string.rfind(filename, '\\')
                if i: filename = filename[i + 1:]
                filename = '%s' % (filename)
                
                objId = indexCheck(container.string2id(filename))
                
                if objId in context.objectIds():
                    continue
                
                context.manage_addProduct['ExtFile'].manage_addExtFile(id=objId, title=filename, descr='', file=REQUEST[key])
                
                context.image2photo()
                
                obj = getattr(context, objId)
                
                # halt upload process if object is empty
                if obj.meta_type == 'Photo':
                    size = obj.size()
                else:
                    size = obj.getSize()
                if size == 0:
                    msg = 'The following file failed to upload: ' + objId
                    context.manage_delObjects(objId)
                    raise Exception, msg
                
                obj.manage_addProperty('submitted_by', username, 'string')
                obj.manage_addProperty('submitted_on', sysTime, 'date')
                
                for usr in context.users_with_local_role('Owner'):
                    obj.manage_addLocalRoles(usr, ('Owner',))
                for usr in context.users_with_local_role('Observer'):
                    obj.manage_addLocalRoles(usr, ('Observer',))
                
                if key in public:
                    roles = context.validRoles()
                    acquire = 1
                else:
                    roles = ['Manager', 'Owner', 'Observer', 'chiefs']
                    acquire = 0
                    
                obj.manage_permission('Access contents information', roles, acquire)
                obj.manage_permission('View', roles, acquire)
                
                addCatObj(objId)
                
                
  # Permissions on objects
    if REQUEST.form['action'] == 'Save':
        public = False
        if REQUEST.form.has_key('public'):
            if REQUEST.form['public']: 
                public = True
            
        groups = []
        if REQUEST.form.has_key('groups'):
            groups = REQUEST.form['groups']
            
        users = []
        if REQUEST.form.has_key('users'):
            users = REQUEST.form['users']
            
        sel_ownGroups = []
        if REQUEST.form.has_key('sel_ownGroups'):
            sel_ownGroups = REQUEST.form['sel_ownGroups']
            
        sel_ownUsers = []
        if REQUEST.form.has_key('sel_ownUsers'):
            sel_ownUsers = REQUEST.form['sel_ownUsers']
            
        sel_obsGroups = []
        if REQUEST.form.has_key('sel_obsGroups'):
            sel_obsGroups = REQUEST.form['sel_obsGroups']
            
        sel_obsUsers = []
        if REQUEST.form.has_key('sel_obsUsers'):
            sel_obsUsers = REQUEST.form['sel_obsUsers']
            
        for i in REQUEST.form['items']:
            obj = getattr(context, i)
            
            objSubBy = None
            if obj.hasProperty('submitted_by'):
                objSubBy = obj.getProperty('submitted_by')
            
            objOldOwns = obj.users_with_local_role('Owner')
            
            for j in groups + users:
                obj.manage_delLocalRoles([j])
                
                if j in sel_ownGroups + sel_ownUsers or (j in objOldOwns and not (user.has_role(['Manager'], obj) or username == objSubBy)):
                    obj.manage_addLocalRoles(j, ('Owner',))
                
                elif j in sel_obsGroups + sel_obsUsers:
                    obj.manage_addLocalRoles(j, ('Observer',))
                    
            if public:
                roles = []
                acquire = 1
            else:
                roles = ['Manager', 'Owner', 'Observer', 'chiefs']
                acquire = 0
                
            obj.manage_permission('Access contents information', roles, acquire)
            obj.manage_permission('View', roles, acquire)
            
            
  # Update Metadata
    if REQUEST.form['action'] == 'Save Changes':
        objId = REQUEST.form['obj_id']
        obj = getattr(context, objId)
        
        meta_items = REQUEST.form['meta_items']
        meta_types = REQUEST.form['meta_types']
        meta_value = REQUEST.form['meta_value']
        
        valParent  = REQUEST.form['valParent']
        
        idxs = []
        oldVals = dict()
        newVals = dict()
        
        if REQUEST.form.has_key('urlExternalLink'):
            url = REQUEST.form['urlExternalLink']
            if url != '':
                if url[0:4] != 'http': url = 'http://' + url
                obj.manage_changeProperties({'urlExternalLink' : url})
                
        
        for id in obj.propertyIds():
            if id in indexes: idxs = idxs + [id]
            
        for i in range(len(meta_items)):
            
            item = meta_items[i]
            type = meta_types[i]
            val0 = meta_value[i]
            valP = valParent[i]
            
            if type == 'date':
                yr = REQUEST.form[item + '_year']
                mt = REQUEST.form[item + '_month']
                dy = REQUEST.form[item + '_day']
                hr = REQUEST.form[item + '_hour']
                me = REQUEST.form[item + '_minute']
                sd = REQUEST.form[item + '_second']
                if yr != '' and mt != '' and dy != '':
                    if val0 != '':
                        dt = DateTime.DateTime(val0)
                        val0 = dt.strftime('%m') + '/' + dt.strftime('%d') + '/' + dt.strftime('%Y') + ' ' + dt.strftime('%X')
                    val1 = mt + '/' + dy + '/' + yr + ' ' + hr + ':' + me + ':' + sd
                else: val1 = ''
            else:
                val1 = REQUEST.form[item]
                
            hldVal1 = string.join(val1).strip()
            
            if type == 'lines': 
                if val1 == '': val1 = []
                else: 
                    rawlist = string.split(val1, ";")
                    val1 = [j.strip() for j in rawlist]
                    while '' in val1: val1.remove('')
                
                if REQUEST.form.has_key('select_' + item):
                    val1 = val1 + REQUEST.form['select_' + item]
                
                rawList = val1
                uniqueList = []
                [uniqueList.append(i) for i in rawList if not uniqueList.count(i)]
                val1 = uniqueList
                val0 = [string.strip(i) for i in string.split(val0, ';')]
                
            if type == 'tokens':
                rawList = string.split(val1)
                uniqueList = []
                [uniqueList.append(i) for i in rawList if not uniqueList.count(i)]
                val1 = string.join(uniqueList, " ")
                
            if type == 'text':
                val1 = val1.replace("&", "&amp;")
                val1 = val1.replace(">", "&gt;")
                val1 = val1.replace("<", "&lt;")
                
            # manage_addProperty() rejects spaces in the id and is caught by valid_property_id(), what a pain...
            item = container.string2id(item)
            
            oldObj = ''
            
            if obj.hasProperty(item):
                oldObj = obj.getProperty(item)
                if val1 == [] or string.join(val1).strip() == '' or hldVal1 == string.join(valP).strip():
                    obj.manage_delProperties([item])
                else:
                    if val0 == val1: continue
                    obj.manage_changeProperties({item : val1})
                    
            elif string.join(val1).strip() != '':
                if val0 == val1: continue
                obj.manage_addProperty(item, val1, type)
                
            oldVals[item] = oldObj
            newVals[item] = val1
            
        addCatObj(objId, idxs=newVals.keys(), oldVals=oldVals, newVals=newVals)


##########################################################################


print context.standard_html_header(context, request)

print '<form action="" method="post" enctype="multipart/form-data" id="objectItems">'

if context.title != "":
  label = context.title
else:
  label = context.getId()

print '<h1>' + label + '</h1>'

path = context.absolute_url(0)

if access:
    print '<div class="documentActions">'
    print '<ul>'
    print '<a href="' + path + '/form_batchUpload" title="Batch file upload">'
    print '<span class="iconsSys batchUpload"></span></a>'
    print '&nbsp;'
    print '<select onchange="window.location.href=this.value">'
    print '<option value="" SELECTED>Add...</option>'
    for i in ['Folder', 'Link']:
        if i == 'Folder':
            selPath = path + '/form_addFolder'
        if i == 'Link':
            selPath = path + '/form_addLink'
        print '<option value="' + selPath + '">' + i + '</option>'
    print '</select>'
    print '</ul>'
    print '</div>'

items1 = context.filterObjectValues(['Folder', 'Photo Folder'])
items2 = context.filterObjectValues(['ExtFile', 'Photo'])

if REQUEST.has_key('size'):
    fSize = container.folderSize(context, ['Folder', 'ExtFile', 'Photo Folder', 'Photo'])
else: fSize = {}

if REQUEST.has_key('sort_on'):
    sort_on = REQUEST.sort_on
else:
    sort_on = 'id'

if REQUEST.has_key('sort_dir'):
    sort_dir = REQUEST.sort_dir
else:
    sort_dir = 'asc'

if sort_on == 'id':
    items = sequence.sort(items1, (('title_or_id', 'nocase', sort_dir),)) + sequence.sort(items2, (('title_or_id', 'nocase', sort_dir),))
elif sort_on in ['get_size', 'content_type']:
    items = sequence.sort(items1, (('title_or_id', 'nocase', sort_dir),)) + sequence.sort(items2, ((sort_on, 'cmp', sort_dir),))
else:
    items = sequence.sort(items1 + items2, ((sort_on, 'cmp', sort_dir),))

sortInfo = '?sort_on=' + sort_on + '&amp;sort_dir=' + sort_dir

print '<table width="100%" cellspacing="0" cellpadding="2"><tr>'

if access:
    print '<th style="white-space:nowrap;width:1%;">'
    print '<input type="checkbox" id="theController" name="theController" title="Select/unselect all" onclick="toggleSelect(\'objectItems\', \'theController\', \'fileList\')" />'
    print '&nbsp;</th>'

print '<th style="width:1%;">'
if REQUEST.has_key('back'):
    print '<a href="javascript:javascript:history.go(-1)" title="Return">'
    print '<span class="iconsSys backOnePage"></span>'
    print '</a>'
else:
    if context.id != 'files':
        print '<a href="' + REQUEST['URL2'] + '" title="Folder up">'
        print '<span class="iconsSys folderUp"></span>'
        print '</a>'
    else:
        print '<img src="' + rootUrl + '/other/opaque.gif" class="logo" width="18" height="16" alt="" />'
print '</th>'

sortPath = path + '?sort_on=content_type'
if sort_on == 'content_type' and sort_dir == 'asc':
    sortPath += '&amp;sort_dir=desc'
print '<th style="white-space:nowrap;width=1%;">&nbsp;<a href="' + sortPath + '">Type</a>&nbsp;</th>'

sortPath = path + '?sort_on=id'
if sort_on == 'id' and sort_dir == 'asc':
    sortPath += '&amp;sort_dir=desc'
print '<th style="width:55%;" align="left"> <a href="' + sortPath + '">Name</a>'

if context.id != 'files':
    print '&nbsp;'
    print '<a href="' + path + '/downloadZip?timeZone=' + timeZone + '" title="Download all">'
    print '<span class="iconsSys downloadAll"></span>'
    print '</a>'

if context.meta_type == 'Photo Folder':
    print '&nbsp;'
    print '<a href="' + path + '/imageGallery" title="Show image gallery">'
    print '<span class="iconsSys imageGallery"></span>'
    print '</a>'
    
print '</th>'
print '<th align="right" style="white-space:nowrap;width:20%;">'

if access:
    print '<a href="' + path + sortInfo + '&amp;size=' + '" title="Show folder size">'
    print '<span class="iconsSys showFolderSize"></span>'
    print '</a>'

sortPath = path + '?sort_on=get_size'
if sort_on == 'get_size' and sort_dir == 'asc':
    sortPath += '&amp;sort_dir=desc'
print '&nbsp;<a href="' + sortPath + '">Size</a>&nbsp;&nbsp;</th>'

sortPath = path + '?sort_on=bobobase_modification_time'
if sort_on == 'bobobase_modification_time' and sort_dir == 'asc':
    sortPath += '&amp;sort_dir=desc'
print '<th style="white-space:nowrap;width:20%;" align="left"> <a href="' + sortPath + '">Last Modified</a></th>'

print '</tr>'

indx = 0
for item in items:
    if indx % 2 != 0:
        print '<tr class="even">'
    else:
        print '<tr class="odd">'
    indx = indx + 1
    
    date = item.bobobase_modification_time().toZone(timeZone)
    
    if item.meta_type in ['Folder', 'Photo Folder']:
        type = item.getProperty('content_type')
        
        if type is None:
            type = 'folder'
            if item.meta_type == 'Photo Folder':
                type += '/image'
                
        fId = item.getId()
        if fId in fSize.keys() and type != 'external/link':
            size = fSize[fId]
        else:
            size = None
        
    elif item.meta_type == 'Photo':
        type = item.content_type()
        size = item.size()
    else:
        type = item.getProperty('content_type')
        size = item.getSize()
        
    owner = []
    local_roles = item.get_local_roles()
    for usr in local_roles:
        if 'Owner' in usr[1]: owner.append(usr[0])
        
    if access:
        if user.has_role(['Manager', 'Owner'], item):
            props = ''
        else:
            props = 'DISABLED'
        print '<td><input type="checkbox" name="file:list" id="fileList" value="' + item.getId() + '" ' + props + ' /></td>'
        
    label = item.title_or_id()
    
    print '<td>'
    print '<button class="iconsSys infoButton" type="submit" name="form_metadata:action" value="' + item.getId() + '"></button>'
    print '</td>'
    
    meta_type = item.meta_type
    address = item.absolute_url(0)
    if meta_type == 'Folder':
        if type == 'external/link':
            meta_type = 'External Link'
            address = item.getProperty('urlExternalLink')
            iconType = 'urlExternalLinkIcon'
        else:
            address += sortInfo
            iconType = 'folder'
    elif meta_type == 'Photo Folder':
        address += sortInfo
        iconType = 'photoFolder'
    else:
        if meta_type == 'Photo':
            address += '?display='
        iconType = ''
        ext = string.rsplit(string.rstrip(label, '.'), '.')
        if ext > 1:
            iconType = string.lower(ext[-1]) + 'Icon'
            
    print '<td align="center">'
    print '<a href="' + address + '" title="' + type + '" >'
    print '<span class="iconsObj ' + iconType + '" ></span>'
    print '</a>'
    print '</td>'
    
    print '<td>'
    print '<a href="' + address + '" >' + label + '</a>'
    if access:
        if context.anonymousHasPermission(item):
            print '<span class="iconsSys publicIcon" title="Public">&nbsp;</span>'
    print '</td>'
    
    
    if size is not None:
        print '<td align="right" style="white-space:nowrap;">'
        print container.fileSize(size)
        print '&nbsp;&nbsp;</td>'
    else:
        print '<td></td>'
    
    print '<td style="white-space:nowrap;">'
    print date.ISO()
    print '</td></tr>'
    
print '</table><p></p>'

print '<p>'

print '<input type="hidden" name="sort_on"  value="' + sort_on  + '" />'
print '<input type="hidden" name="sort_dir" value="' + sort_dir + '" />'

if access:
    print '<fieldset class="submit">'
    print '<input type="submit" name="cut"    value="Cut" />'
    print '<input type="submit" name="copy"   value="Copy" />'
    print '<input type="submit" name="paste"  value="Paste" />'
    print '<input type="submit" name="delete" value="Delete" />'
    print '<input type="submit" name="form_rename:action" value="Rename" />'
    print '<input type="submit" name="form_permissions:action" value="Permissions" />'
    print '</fieldset>'
    
    publicStatus = ''
    if not context.anonymousHasPermission(context):
        publicStatus = 'DISABLED'
    print '<fieldset class="submit">'
    print '<input type="checkbox" name="public:list" value="file.name' + str(1) + '" title="Grant anonymous users view/access permissions"' + publicStatus + ' />'
    print '<input type="file" name="file.name' + str(1) + '" size="25" />'
    print '<input type="submit" name="action" value="Upload" />'
    print '</fieldset>'

print '</p>'
print '</form>'

print context.standard_html_footer(context, request)

return printed
