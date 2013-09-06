## Script (Python) "form_metaFields"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request  = container.REQUEST
REQUEST  = context.REQUEST

# sorting function

def sortedDictValues(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

# alphabet string

alphabet = 'abcdefghijklmnopqrstuvwxyz'

# current catalog indexes

indexes = container.catalog.indexes()

# fields; name, category, type

N0 = list(container.files.getProperty('metaTitle'))
C0 = list(container.files.getProperty('metaCategory'))
T0 = list(container.files.getProperty('metaTypes'))

# available field types and those field names which are unavailable

types = list(container.files.getProperty('types'))
unavailable = list(container.files.getProperty('unavailable'))

# button action; add a field

if REQUEST.form.has_key('fieldAdd'):
    n1 = REQUEST.form['namField']
    c1 = REQUEST.form['catFieldnew']
    c2 = REQUEST.form['catField']
    t1 = REQUEST.form['typField']
    
    if (n1 != '') and (c1 != '' or c2 != ''):
        if (n1 not in (N0 + unavailable)):
            N = n1
            T = t1
            if c1 == '': C = c2
            else:        C = c1
            
            # locate index for last field in category
            
            k = 0
            for i in range(len(N0)):
                if C == C0[i]: k = i
            if k == 0: k = len(N0)
            
            N0.insert(k + 1, N)
            C0.insert(k + 1, C)
            T0.insert(k + 1, T)

# button action; update categories

elif REQUEST.form.has_key('catUpdate'):
    
    catOld = REQUEST.form['catNAMEold']
    
    # priority sort of categories
    
    Pri = [str(x) for x in REQUEST.form['catPRIORITY']]
    Key = {}
    for i in range(len(catOld)):
        Key[Pri[i] + alphabet[i]] = catOld[i]
    Sorted = sortedDictValues(Key)
    
    N = []; C = []; T = []
    for i in Sorted:
        for j in range(len(C0)):
            if i == C0[j]: 
                N = N + [N0[j]]
                C = C + [C0[j]]
                T = T + [T0[j]]
    N0 = N; C0 = C; T0 = T
    
    # remove categories
    
    if REQUEST.form.has_key('catREMOVE'):
        catRemove = REQUEST.form['catREMOVE']
        for i in range(len(C0)-1, -1, -1):
            if C0[i] in catRemove: 
                N0.pop(i)
                C0.pop(i)
                T0.pop(i)
                
    # rename categories
    
    catNew = REQUEST.form['catNAMEnew']
    for i in range(len(C0)):
        for j in range(len(catOld)):
            if C0[i] == catOld[j]: C0[i] = catNew[j]
            
# update fields

elif REQUEST.form.has_key('fieldUpdate'):
    
    # unique categories based on old list
    
    catUnique = []
    for i in C0: 
        if i not in catUnique: catUnique.append(i)
        
    # new category list
    
    C0 = REQUEST.form['CATEGORY']
    
    # priority sort of fields
    
    Pri = [str(x) for x in REQUEST.form['PRIORITY']]
    Sorted = []
    for i in catUnique:  
        Key = {}
        k = 0
        for j in range(len(N0)):
            if i == C0[j]:
                k = k + 1 
                Key[Pri[j] + alphabet[j]] = N0[j]
        Sorted = Sorted + sortedDictValues(Key)
        
    N = []; C = []; T = []
    for i in Sorted:
        for j in range(len(N0)):
            if i == N0[j]: 
                N = N + [N0[j]]
                C = C + [C0[j]]
                T = T + [T0[j]]
    N0 = N; C0 = C; T0 = T
    
    # remove fields
    
    if REQUEST.form.has_key('REMOVE'):
        fieldRemove = REQUEST.form['REMOVE']
        for i in range(len(N0)-1, -1, -1):
            if N0[i] in fieldRemove: 
                N0.pop(i)
                C0.pop(i)
                T0.pop(i)
                
    # index selected fields in catalog
    
    NN0 = []
    for i in range(len(N0)):
        NN0 = NN0 + [container.string2id(N0[i])]
        
    if REQUEST.form.has_key('INDEX'):
        fieldIndex = REQUEST.form['INDEX']
        for i in range(len(N0)):
            
            if (NN0[i] in indexes) and (N0[i] not in fieldIndex):
                container.catalog.manage_delIndex(NN0[i])
                
            if (NN0[i] not in indexes) and (N0[i] in fieldIndex): 
                if   T0[i] == 'date':  
                    indxType = 'DateIndex'
                elif T0[i] == 'text':  
                    indxType = 'TextIndex'
                elif T0[i] == 'lines' or T0[i] == 'tokens': 
                    indxType = 'KeywordIndex'
                else:
                    indxType = 'FieldIndex'
                    
                container.catalog.manage_addIndex(NN0[i], indxType)
                
        indexes = container.catalog.indexes()
        
    # remove all indexes not in the fields list
    
    for i in indexes:
        if i not in NN0 + unavailable: container.catalog.manage_delIndex(i)
        

# update all indexes in the search catalog

elif REQUEST.form.has_key('updateCatalog'):
    container.catalog.refreshCatalog(clear=1)

# update properties in files object

if REQUEST.form.has_key('fieldAdd') or REQUEST.form.has_key('catUpdate') or REQUEST.form.has_key('fieldUpdate'):
    container.files.manage_changeProperties({'metaTitle'    : N0})
    container.files.manage_changeProperties({'metaCategory' : C0})
    container.files.manage_changeProperties({'metaTypes'    : T0})
    
# unique categories based on new list

catUnique = []
for i in C0:
    if i not in catUnique:
        catUnique.append(i)
        


#####################################################

# header

print context.standard_html_header(context, request)

# title

print '''
    <h1>Metadata Management</h1>
    <p></p>
    <form action="" method="post">
'''

# add field

print '<h3>Add Field</h3>'

print '<table width="100%" cellspacing="0" cellpadding="2" border="0">'

print '<tr><th style="width:1%;"></th><th style="width:99%;"></th></tr>'

print '<tr class="odd"><td align="right">Name:</td>'
print '<td><input type="text" name="namField" value="" /></td></tr>'

print '<tr class="odd"><td align="right">Category:</td>'
print '<td><input type="text" name="catFieldnew" value="" />'
print '<select name="catField">'
print '<option value="">or choose...</option>'
for i in catUnique:
    print '<option>' + i + '</option>'
print '</select>'
print '</td></tr>'

print '<tr class="odd"><td align="right">Type:</td>'
print '<td><select name="typField">'
for i in types:
    print '<option>' + i + '</option>'
print '</select>'
print '</td></tr>'

print '</table>'

print '<p><input type="submit" name="fieldAdd" value=" Add " /></p>'


# category management


print '<h3>Categories</h3>'
print '<table width="100%" cellspacing="0" cellpadding="2" border="0">'
print '<tr>'
print '<th style="width:1%;">Priority</th>'
print '<th style="width:1%;">Remove</th>'
print '<th style="width:98%;" align="left">Category</th></tr>'

for i in range(len(catUnique)):
    cat = catUnique[i]
    print '<tr class="odd">'
    print '<td align="center"><input type="text" name="catPRIORITY:list" value="' + str(i + 1) + '" size="1" maxlength="2" /></td>'
    print '<td align="center"><input type="checkbox" name="catREMOVE:list" value="' + cat + '" /></td>'
    print '<td align="left">  <input type="text" name="catNAMEnew:list"  value="' + catUnique[i] + '" /></td></tr>'
    print '<input type="hidden" name="catNAMEold:list" value="' + cat + '" />'
    
print '</table>'

print '<p><input type="submit" name="catUpdate" value="Update" /></p>'


# field management


print '<h3>Meta Fields</h3>'
print '<table width="100%" cellspacing="0" cellpadding="2" border="0">'
print '<tr>'
print '<th style="width:1%;">Priority</th>'
print '<th style="width:1%;">Remove</th>'
print '<th style="width:1%;" align="left">Category</th>'
print '<th style="width:1%;">Search</th>'
print '<th style="width:8%;">Type</th>'
print '<th style="width:88%;" align="left">Name</th>'
print '</tr>'

idx = []
flag = True; style = 0
for i in range(len(catUnique)):
    idx = idx + [0]
    cat = catUnique[i]

    if flag: 
        flag = False
        style = (style + 1) % 2
        
    for j in range(len(N0)):
        if C0[j] == cat:
            idx[i] = idx[i] + 1

            flag = True
            if style == 0: col = ''
            else: col = 'class="inputCol"'

            print '<tr class="odd">'

            print '<td align="center"><input type="text" name="PRIORITY:list" value="' + str(idx[i]) + '" size="1" maxlength="2" ' + col + ' /></td>'
            print '<td align="center"><input type="checkbox" name="REMOVE:list" value="' + N0[j] + '" /></td>'

            print '<td><select name="CATEGORY:list">'
            for k in catUnique:
                if k == C0[j]:
                    print '<option selected="selected">' + k + '</option>'
                else: print '<option>' + k + '</option>'
            print '</select>'
            print '</td>'

            if container.string2id(N0[j]) not in indexes:
                checked = ''
            else:
                checked = 'checked="checked"'
            print '<td align="center"><input type="checkbox" ' + checked + ' name="INDEX:list" value="' + N0[j] + '" /></td>'

            print '<td align="center">' + T0[j] + '</td>'

            print '<td>' + N0[j] + '</td>'

            print '</tr>'

print '</table>'

# closing buttons

print '<p>'
print '<input type="submit" name="fieldUpdate" value="Update" />'
print '<input type="submit" name="updateCatalog" value="Update Catalog" />'
print '<input type="reset" value="Reset" />'
print '</p>'
print '</form>'

# footer

print context.standard_html_footer(context,request)

return printed
