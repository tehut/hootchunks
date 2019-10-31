import os
import sys 
import select
import hootchunk
import io
import mmh3
from hootchunk import hooterrors 

from pymemcache import serde
from pymemcache.client.base import Client

def return_file_hash(file_addy):
    file_size = (os.stat(file_addy).st_size / (10 ** 6))
    if file_size > 50:
        print(f"hootlib requires files be smaller than 50MB. Your file is {file_size} MB. \nPlease try again with a smaller file")
        raise Error("File too large")
    else:
        with open(file_addy, "rb") as f: 
            contents = f.read()
    return mmh3.hash(contents, signed=False)

def chunk_file(file_addy, checksum, chunk_size=999):
    chunks = []
    result = None
    with open(file_addy, 'rb' ) as f:
        while result != b'':
            result = f.read(chunk_size)
            chunks.append(result)
    # compare hash values before writing to cache
    ready = read_chunks_to_bites(chunks, len(chunks), file_addy).getvalue()
    chunked_checksum = mmh3.hash(ready, signed=False)
    check_the_sums(checksum, chunked_checksum)
    return chunks

def create_client(service_ip="none"):
    client = Client ((service_ip, 11211), serializer=serde.python_memcache_serializer, deserializer=serde.python_memcache_deserializer)
    return client 

def get_input(message="Three second response timeout: aborting cache write"):
    i, o, e = select.select( [sys.stdin], [], [], 3 )
    if (i):
        user_response = sys.stdin.readline().strip()
        return user_response
    else:
        raise Error(message)
    
def check_cache(key, checksum, chunks, client, cache_limit=50, update=False):
    # client = create_client()
    values = client.stats()
    megabyte_multiplier = (10 ** 6)

    # Confirm there's room in the cache
    stat_values = {k.decode("utf-8") : v for k,v in values.items()}
    used_bytes =int(stat_values.get('bytes'))
    total_bytes =int(stat_values.get('limit_maxbytes'))
    fifty_mb_in_bytes =( cache_limit * megabyte_multiplier)

    if (total_bytes - used_bytes) < fifty_mb_in_bytes:
        raise hooterror.CacheFullError("Less than 50mb available in cache, unable to file")
    else:
        print(f"Used {used_bytes} of {total_bytes} available, continuing with cache write ")
    
    # Confirm the key isn't already in cache, unless called by Update
    if update == False:
        preset_value = client.get(f"{key}:hash")
        if (preset_value is not None and preset_value[0] == checksum):
            raise hooterrors.KeyCollision("The key and value associated with your request are already in the cache")

        elif preset_value is not None and preset_value[0] != checksum:
            print(f"The key:{key} was found in the cache with an unexpected value. \n") 
            print("Type \"y\" to overwrite the existing value. Do nothing to abort cache write.")
            user_response = get_input()

            if user_response is None or user_response != "y": 
                print("Exiting hootcache")
                raise hooterrors.KeyCollision("The key associated with your request was located in the cache with an unexpected value")
        else:
            pass


def cache_chunks(key, checksum, chunks, client):
    key_value ="{}:hash".format(key).strip(' ')
    list_length = len(chunks)
    value_value = (checksum,list_length)
    key_response=(client.set(key_value, value_value, noreply=False))
    
    if key_response == False:
        raise hooterrors.CacheWrite()
    set_list = {f"{key}:{index}": chunk for index, chunk in enumerate(chunks)}
    if list_length == len(set_list):
        unapplied_chunks = (client.set_many(set_list, noreply=False))
    else: 
        raise hooterrors.CacheWrite()

    if len(unapplied_chunks) > 0:
        client.delete_many(set_list)
        client.delete(key_value)
        raise hooterrors.CacheWrite()


def read_chunks_to_bites(chunk_list, length_original, key):
    f = io.BytesIO()
    if type(chunk_list) == list:
        for i in range(0, len(chunk_list), 1):
            f.write(chunk_list[i])
    elif type(chunk_list) == dict:
        for i in range(0, length_original, 1):
            f.write(chunk_list[f"{key}:{i}"])
    return f

def check_the_sums(original_hash, new_hash):
    if original_hash != new_hash:
        raise hooterrors.CacheRead("Chunking error, hashes don't match")
        
def UpdateCache(file_addy, serviceIP='localhost'):
    WriteToCache(file_addy, serviceIP, True)

def WriteToCache(file_addy, serviceIP='localhost', update=False):
    client = create_client(serviceIP)    
    if '/tmp/' in file_addy:
        key = file_addy.replace('/tmp/', '')
    checksum = return_file_hash(file_addy)
    chunked_file = chunk_file(file_addy, checksum)
    check_cache(key, checksum, chunked_file, client)
    cache_chunks(key, checksum, chunked_file, client)
    client = create_client()
    client.close()
    return f"{key}:{checksum}"

def ReadFromCache(key, serviceIP='localhost'):
    client = create_client(serviceIP)
    c_values = client.get(f"{key}:hash")

    if c_values is None:
        raise hooterrors.CacheRead("Value not found in the cache")
    length = int(c_values[1])
    original_hash = c_values[0]

    read_list =[(f"{key}:{i}") for i in range(0, length,1)]
    file_chunks = client.get_many(read_list)
    file_stream = read_chunks_to_bites(file_chunks, length, key).getvalue() 
    stream_hash = mmh3.hash(file_stream, signed=False)
    check_the_sums(original_hash, stream_hash)
    client.close()
    return file_stream

def FlushCache(serviceIP='localhost'):
    client = create_client(serviceIP)
    client.flush_all()
    client.close()

def CreateClient(serviceIP='localhost'):
    client = create_client(serviceIP)
    return client

def DeleteKey(key, serviceIP='localhost'):
    client = create_client(serviceIP)
    response = client.delete(key)
    print(response)
    client.close()
    return response
