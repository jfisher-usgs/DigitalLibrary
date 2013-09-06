## Script (Python) "index_html"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=q='', type='Site'
##title=
##
request  = container.REQUEST
REQUEST  = context.REQUEST

if REQUEST.form.has_key('q'):
    q = REQUEST.form['q']
    
useDefaults = False
if REQUEST.form.has_key('button') and REQUEST.form['button'] != 'Clear':
    useDefaults = True
    
numResults = range(10, 100, 10)

#####################################################

print container.standard_html_header(context, request)

print '<form method="get" action="">'

print '<h1>' + type + ' Search</h1>'

if type == 'Site':
    print '<fieldset>'
    print '<ol>'
    print '<li>'
    print '<input type="text" name="q" id="q" value="' + q + '" size="30" />'
    print '</li>'
    print '</ol>'
    print '</fieldset>'
    
    print '<fieldset>'
    print '<input type="submit" name="button" value="Search" />&nbsp;'
    print '<a href="' + context.absolute_url() + '/index_html?type=Advanced">Advanced</a>'
    print '</fieldset>'
    
if type == 'Advanced':
    
    print '<p></p>'
    print '<table cellspacing="0" cellpadding="2" border="0">'
    
    # current catalog indexes
    indexes = container.catalog.indexes()
    
    # fields; name, category, type
    N0 = ['Name', 'Type', 'Submitted by', 'Submitted on', 'Last Modified'] + list(container.files.getProperty('metaTitle'))
    T0 = ['text', 'lines', 'lines', 'date', 'date'] + list(container.files.getProperty('metaTypes'))
    
    idx = []
    if REQUEST.form.has_key('indexes'):
        idx = REQUEST.form['indexes']
        
    for i in range(len(N0)):
        
        if N0[i] == 'Type':
            N = 'content_type'
        elif N0[i] == 'Submitted by':
            N = 'submitted_by'
        elif N0[i] == 'Submitted on':
            N = 'submitted_on'
        elif N0[i] == 'Last Modified':
            N = 'bobobase_modification_time'
        else:
            N = string.join(string.split(N0[i]), "_")
            
        if N in indexes:
            
            checked = ''
            if N in idx  and useDefaults:
                checked = 'checked="checked"'
                
            defaultValue = ''
            if REQUEST.form.has_key(N) and useDefaults:
                defaultValue = REQUEST.form[N]
            elif REQUEST.form.has_key(N + '_year') and useDefaults:
                yr = REQUEST.form[N + '_year']
                mt = REQUEST.form[N + '_month']
                dy = REQUEST.form[N + '_day']
                defaultValue = mt + '/' + dy + '/' + yr
                
                
            print '<tr>'
            print '<td style="white-space:nowrap;" align="right">' + N0[i] + ':</td>'
            print '<td align="center"><input type="checkbox" name="indexes:list" value="' + N + '" ' + checked + ' /></td>'
            print '<td>'
            
            if T0[i] == 'lines':
                print '<select name="' + N + '">'
                
                for j in container.catalog.uniqueValuesFor(N):
                    selected = ''
                    if j == defaultValue and useDefaults:
                        selected = 'selected="selected"'
                        
                    if N0[i] == 'Submitted by':
                        hld = getattr(container.people, j, None)
                        if hld and hld.hasProperty('name_first'):
                            print '<option value="' + j + '" ' + selected + '>' + hld.title + '</option>'
                    else:
                        print '<option ' + selected + '>' + j + '</option>'
                    
                print '</select>'
                
            elif T0[i] in ['date', 'float', 'int']:
                    
                if T0[i] == 'date':
                    dicPeriod = {'before': 'max', 'after': 'min'}
                else:
                    dicPeriod = {'before': 'min', 'after': 'max'} 
                    
                defaultPeriod = None
                if REQUEST.form.has_key('Period_' + N): 
                    defaultPeriod = REQUEST.form['Period_' + N]
                    
                print '<select name="Period_' + N + '" >'
                for j in dicPeriod.keys():
                    selected = ''
                    if dicPeriod[j] == defaultPeriod and useDefaults:
                        selected = 'selected'
                    print '<option value="' + dicPeriod[j] + '" ' + selected + '>' + j + '</option>'
                print '</select>'
                
                print '&nbsp;&nbsp;&nbsp;'
                
                if T0[i] == 'date':
                    print container.dateTime(N, defaultValue, includeTime=False)
                else:
                    print '<input type="text" name="' + N + '" size="10" value="' + defaultValue + '" />'
                    
            else:
                print '<input type="text" name="' + N + '" size="35" value="' + defaultValue + '" />'
                
            print '<a class="tooltip" title="' + container.help(key="Search", typ=T0[i]) + '">'
            print '<span class="iconsSys helpIcon" ></span>'
            print '</a>'
            
            print '</td></tr>'
            
    print '<tr><td></td><td></td><td style="padding-top:0.75em;">'
    print '<input type="submit" name="button" value="Search" />'
    print '<input type="submit" name="button" value="Clear" />'
    print '<input type="reset"  name="button" value="Reset" />'
    
    print '<input type="hidden" name="type" value="' + type + '" />'
    
    defaultValue = ''
    if REQUEST.form.has_key('numresults') and useDefaults:
        defaultValue = REQUEST.form['numresults']
        
    print '<select name="numresults">'
    for num in numResults:
        selected = ''
        if str(num) == defaultValue:
            selected = 'selected="selected"'
        print '<option ' + selected + ' value="' + str(num) + '">' + str(num) + ' results</option>'
    print '</select>'
    
    print '</td></tr></table>'
    
print '</form>'

#####################################################

if type == 'Site' and q != '':
#   kw = {'TextIdx' : q, 'meta_type' : 'DTML Document', 'sort_limit' : 100}
#   results = context.catalog(kw)
    kw = {'Name' : q, 'meta_type' : ['DTML Document', 'ExtFile', 'Photo', 'Folder', 'Photo Folder'], 'sort_limit' : 100}
    results = context.catalog(kw)
    
elif type == 'Advanced' and useDefaults and REQUEST.form.has_key('indexes'):
    
    kw = {'meta_type' : ['ExtFile', 'Photo', 'Folder', 'Photo Folder']}
    for i in REQUEST.form['indexes']:
        
        if REQUEST.form.has_key(i + '_year'):
            yr = REQUEST.form[i + '_year']
            mt = REQUEST.form[i + '_month']
            dy = REQUEST.form[i + '_day']
            val = mt + '/' + dy + '/' + yr
            
        else:
            val = REQUEST.form[i]
            
        tmp = {'query' : val}
        if REQUEST.form.has_key('Period_' + i):
            tmp['range'] = REQUEST.form['Period_' + i]
            
        kw[i] = tmp
        
    maxResults = int(REQUEST.form['numresults'])
    kw['sort_limit'] = maxResults
    results = context.catalog(kw)[:(maxResults + 1)]
    
else:
    results = None

#####################################################

if results != None:
    
    print '<table width="100%" cellspacing="0" cellpadding="2" border="0">'
    print'<tr><th style="width:1%;"><th style="width:99%;"></tr>'
    
    indx = 0
    for result in results:
        
        access = result.aq_parent.restrictedTraverse(result.getPath(), None)
        
        if access:
            if indx % 2 != 0:
                print '<tr>'
            else:
                print '<tr bgcolor="#F7F9FA">'
            indx = indx + 1  
            
            
            label = result.id
            if result.title != '':
                label = result.title
            
            meta_type = result.meta_type
            address = result.absolute_url
            content_type = result.content_type
            if meta_type == 'Folder':
                if result.content_type == 'external/link':
                    meta_type = 'External Link'
                    address = result.urlExternalLink
                    iconType = 'urlExternalLinkIcon'
                else:
                    iconType = 'folder'
            elif meta_type == 'Photo Folder':
                iconType = 'photoFolder'
            elif meta_type == 'DTML Document':
                iconType = 'htmlIcon'
                content_type = 'text/html'
            else:
                if meta_type == 'Photo':
                    address += '?display='
                iconType = ''
                ext = string.rsplit(string.rstrip(label, '.'), '.')
                if ext > 1:
                    iconType = string.lower(ext[-1]) + 'Icon'
                        
            print '<td valign="middle" align="center"><p>'
            print '<a href="' + address + '" title="' + content_type + '" >'
            print '<span class="iconsObj ' + iconType + '" ></span>'
            print '</a><br></p></td>'
            
            print '<td><p>'
            print '<a href="' + address + '">' + label + '</a><br>'
                
            hld = string.split(result.absolute_url, sep="/")
            p1 = string.join(hld[0:-2], "/") + "/"; p2 = hld[-2]; p3 = "/" + hld[-1]
            
            print '<span class="addressUrl">' + p1 + '<a href="' + p1 + p2 + '?back=1">' + p2 + '</a>' + p3 + '</span>'
            
            print '</p></td></tr>'
            
    if indx == 0: 
        msg = 'There was no data matching this query.'
        print '<tr><td colspan=2><font color="#FF0000">' + msg + '</font></td></tr>'
        
    print '</table>'

#####################################################

if type == 'Site':
    print '<script type="text/javascript">setDefaultFocus(\'q\');</script>'

print container.standard_html_footer(context, request)

return printed
