testing = __name__ == '__main__'

import zipfile
import cStringIO
import tempfile
import os
import string

if not testing:
       import AccessControl
       import Globals
       import syslog

def ZipInfo(filename, date_time=None):
       return zipfile.ZipInfo(filename, date_time)

class _ZipFile(zipfile.ZipFile):
       # I hate hardcoding.  This should be in the ZODB and filesystem.
       download_url_base = '/root03/temp/zipfile_downloads'
       download_dir_base = '/var/www/temp/zipfile_downloads'

       if not testing:
               security = AccessControl.ClassSecurityInfo()
               security.declareObjectPublic()
               security.declarePublic(
                       'writestr',
                       'writeobj',
                       'close',
                       'get_download_url',
               )

       def __init__(self, contents=None, filename='package.zip'):
               if contents:
                       self.fp0 = cStringIO.StringIO()
                       self.fp0.write(contents)
                       zipfile.ZipFile.__init__(self, self.fp0, 'r')
               else:
                       #self.fp0 = open('/tmp/foo.zip', 'w')
                       #zipfile.ZipFile.__init__(self, self.fp0, 'w')

                       # Create a temporary file because we'll access this directly later.
                       #(ignore, self.zip_filename) = tempfile.mkstemp(prefix='temp-', suffix='.zip', dir=self.download_dir_root + self.download_dir)
                       self.download_path = tempfile.mkdtemp(dir=self.download_dir_base)
                       #os.chown(self.download_path, -1, self.zip_gid)
                       os.chmod(self.download_path, 0755)

                       self.zip_filename = self.download_path + '/' + filename
                       zipfile.ZipFile.__init__(self, self.zip_filename, 'w')

       def __del__(self):
               # I should do something better but I don't know what.
               None

       def close(self):
               # If just reading the zip file, simply close it.
               if self.mode == 'r':
                       return(zipfile.ZipFile.close(self))

               # trick in order to keep from closing the file before we read it
               self._filePassed = True

               zipfile.ZipFile.close(self)

               # Set so that Web server will be able to read the file.
               os.chmod(self.zip_filename, 0644)

               return(0)

               # These operations were required when using stringIO.
               zip_data = self.fp0.getvalue()
               self.fp0.close()
               self.fp0 = None
               return(zip_data)

       def get_download_url(self, request):
               return(str(request['BASE0'] + self.download_url_base + '/' + string.join(self.zip_filename.split('/')[-2:], '/')))
               return(self.zip_filename)

       # forbidden methods
       #_write = write
       #write = None
       #writepy = None

       def writeobj(self, obj, arcname=None):
               # Check if this user has access to this object.
               if not AccessControl.getSecurityManager().checkPermission('View', obj):
                       raise 'Unauthorized', 'not authorized to View %s' % (obj.absolute_url())

               if hasattr(obj, '_original'):
                       fsname = obj._original._get_fsname(obj._original.filename)
               elif hasattr(obj, '_get_fsname'):
                       fsname = obj._get_fsname(obj.filename)
               else:
                       raise Exception, 'Can not determine filename for object.'

               self.write(filename=fsname, arcname=arcname)

def ZipFile(contents=None, filename=None):
       return(_ZipFile(contents=contents, filename=filename))

if not testing:
       Globals.InitializeClass(_ZipFile)
       AccessControl.allow_class(_ZipFile)
       