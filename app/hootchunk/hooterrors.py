class Error(Exception):
   "Base class for other exceptions"
   pass
   
class KeyCollision(Error):
   "Raised when the target key already exists in the cache"
   pass

class CacheFull(Error):
   "Raised when the cache is at memory limit"
   pass
  
class CacheWrite(Error):
   "Raised there was a problem writing to the cache. Your file has not been added"""
   pass

class CacheRead(Error):
   "Raised there was a problem reading from the cache"
   pass

class FileSize(Error):
   "File is too large"
   pass




