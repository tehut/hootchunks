## HootCache API 
### powered by hootchunk lib 


## Usage
### Run
With extant minikube cluster

    - source run.sh
    - run
    
Build minikube cluster

    - source run.sh
    - launch_cluster
    - run

The last line of the run command will output the base endpoint open as a NodePort on your cluster

## Endpoints
- base url: host/hootcache/api/v1.0/files
- get(): returns `cached_files` list of files added since launch of api
- get(/files/<file-name>): returns stream of file contents
- post(/files/<file-name>): posts file, returns key and adds it to `cached_files` list
    
### Cleanup
    - source run.sh
    - clean_services
    - clean_cluster
    
    
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



  
