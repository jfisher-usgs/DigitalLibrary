## Script (Python) "image2photo"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
"""
Convert images to Photo objects.
"""

if context.meta_type == 'Photo Folder':
    factory = context.manage_addProduct['Photo'].manage_addProduct['ExtFile']
    for obj in context.objectValues(['ExtFile']):
        if string.split(obj.getProperty('content_type'), "/")[0] == 'image':
            
            owns = obj.users_with_local_role('Owner')
            obrs = obj.users_with_local_role('Observer')
            
            imgId = obj.getId()
            
            context.manage_delObjects([imgId,])
            factory.manage_addPhoto(imgId, obj.title, obj, store="ExtImage", engine="ImageMagick", pregen="1", quality="100")
            
            obj = getattr(context, imgId)
            for usr in owns:
                obj.manage_addLocalRoles(usr, ('Owner',))
            for usr in obrs:
                obj.manage_addLocalRoles(usr, ('Observer',))

return
