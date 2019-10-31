## HootCache API 
### powered by hootchunk lib 


## Usage
### Run
*  `source run.sh`
* `run local`

## Endpoints
- base url: host/hootcache/api/v1.0/files
- get(): returns `cached_files` list of files added since launch of api: ` curl <host>/hootcache/api/v1.0/files`
- get(/files/<file-name>): returns stream of file contents: `<host>/hootcache/api/v1.0/files/<filename`
- post(/files/<file-name>): posts file, returns key and adds it to `cached_files` list: ` <host>/hootcache/api/v1.0/files/<filename>`
    
    
## Repo Contents
- root:
    - `run.sh` script
    - hootcache service Dockerfile
    - `hootcache.yml` pod configuration

- app:
    - app.py 
    - requirements.txt file for hootcache api
    - `test` dir for hootcache api
    - flask & hootchunk libraries

- hootchunk
    - `hootchunk.py` memcached wrapper library
    - `hooterrors.py` errors specific to hootchunk lib
    - `test` test dir for hootchunk lib



  
