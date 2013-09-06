## Script (Python) "downloadZip"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=timeZone='Universal',debug=False
##title=
##
import DateTime
sysTime = DateTime.DateTime(timeZone)
fmtDate = sysTime.strftime('%Y') + sysTime.strftime('%m') + sysTime.strftime('%d')

name = context.title_or_id()
folder = '/' + name
ZipName = container.string2id(name + ' ' + fmtDate + '.zip')

zf = context.zipfile_ZipFile(filename=ZipName)

# recursively iterate through objects within a folder
def recursiveObjs(context, folder, objs):
    for obj in objs:
        if obj.meta_type in ['ExtFile', 'ExtImage', 'Photo']:
            filename = folder + '/' + obj.title_or_id()
            zf.writeobj(obj, filename)
            print obj.absolute_url, filename
            
        elif obj.meta_type in ['Folder', 'Photo Folder']:
            print 'traverse %s' % (obj.absolute_url())
            newFolder = folder + '/' + obj.title_or_id()
            newObjs = obj.filterObjectValues(['Folder', 'ExtFile', 'Photo Folder', 'Photo'])
            recursiveObjs(obj, newFolder, newObjs)
            
        else:
            print 'skipped %s' % (obj.meta_type)

    return(printed)

objs = context.filterObjectValues(['Folder', 'ExtFile', 'Photo Folder', 'Photo'])

print recursiveObjs(context, folder, objs)

zf.close()

if debug:
    print 'done'
    return(printed)

url = zf.get_download_url(context.REQUEST)
context.REQUEST.response.redirect(url)

return printed
