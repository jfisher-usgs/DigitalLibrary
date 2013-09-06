## Script (Python) "metaExport"
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
RESPONSE = request.RESPONSE

import DateTime

ROOT = container.root()
rootUrl = ROOT.absolute_url() + '/files'

objId = REQUEST.form['obj_id']
obj = getattr(context, objId)

filename = objId + '.csv'

cr = chr(13) + chr(10)
text = '#Name,Type,Value' + cr

valueDict ={}
for item in obj.propertyItems():
    valueDict[item[0]] = item[1]
    
for idType in obj.propertyMap():
    text += str(idType['id']) + ',' + str(idType['type']) + ',' + str(valueDict[idType['id']]) + cr
    
RESPONSE.setHeader("Content-type", "text/csv")
RESPONSE.setHeader("Content-disposition", "inline; filename=" + filename)

return text
