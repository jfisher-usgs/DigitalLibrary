## Script (Python) "recursiveUpdate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=object, catObj=True, update_metadata=1, idxs=None, oldVals=None, newVals=None
##title=
##
for obj in object.objectValues():
    
    if idxs: Idxs = [i for i in idxs if i in obj.propertyIds()]
    else:    Idxs = None
    
    if catObj: 
        if Idxs:
            for idx in Idxs:
                pro = obj.getProperty(idx)
                typ = obj.getPropertyType(idx)
                
                oldVal = oldVals[idx]
                newVal = newVals[idx]
                
                if oldVal == '': continue
                
                val = None
                
                if typ == 'date':
                    if newVal == '': continue
                    
                    if not isinstance(newVal, DateTime): newVal = DateTime(newVal)
                    
                    oldT = []
                    newT = []
                    proT = []
                    valT = []
                    
                    oldT += [oldVal.strftime('%Y')]
                    oldT += [oldVal.strftime('%m')]
                    oldT += [oldVal.strftime('%d')]
                    oldT += [oldVal.strftime('%H')]
                    oldT += [oldVal.strftime('%M')]
                    oldT += [oldVal.strftime('%S')]
                    
                    newT += [newVal.strftime('%Y')]
                    newT += [newVal.strftime('%m')]
                    newT += [newVal.strftime('%d')]
                    newT += [newVal.strftime('%H')]
                    newT += [newVal.strftime('%M')]
                    newT += [newVal.strftime('%S')]
                    
                    proT += [pro.strftime('%Y')]
                    proT += [pro.strftime('%m')]
                    proT += [pro.strftime('%d')]
                    proT += [pro.strftime('%H')]
                    proT += [pro.strftime('%M')]
                    proT += [pro.strftime('%S')]
                    
                    for i in range(6):
                        if oldT[i] == proT[i]: valT += [newT[i]]
                        else:                  valT += [proT[i]]
                        
                    val = DateTime(int(valT[0]), int(valT[1]), int(valT[2]), int(valT[3]), int(valT[4]), int(valT[5]))
                    val = val.strftime('%x') + ' ' + val.strftime('%X')
                    
                if typ in ['string', 'text', 'float', 'int', 'date']:
                    
                    if string.find(str(pro), str(oldVal)) >= 0:
                        
                        val = string.replace(str(pro), str(oldVal), str(newVal))
                        val = string.strip(val)
                        
                if typ in ['lines', 'tokens']:
                    if typ == 'tokens': 
                        if isinstance(oldVal, str): oldVal = string.split(oldVal)
                        if isinstance(newVal, str): newVal = string.split(newVal)
                        
                    rawList = newVal + [i for i in pro if i not in oldVal]
                    uniqueList = []
                    [uniqueList.append(i) for i in rawList if not uniqueList.count(i)]
                    val = uniqueList
                    
                if val:
                    if val == [] or val == '': obj.manage_delProperties([idx])
                    else: obj.manage_changeProperties({idx : val})
                    
        container.catalog.catalog_object(obj, idxs=idxs, update_metadata=update_metadata)
        
    else:
        uid = '/'.join(obj.getPhysicalPath())
        container.catalog.uncatalog_object(uid)
        
    if obj.meta_type in ['Folder', 'Photo Folder']:
        container.recursiveUpdate(obj, catObj, update_metadata, idxs, oldVals=oldVals, newVals=newVals)
