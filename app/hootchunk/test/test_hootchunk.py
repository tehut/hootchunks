
import pytest
import sys, os, tempfile, io
from hootchunk import hootchunk 
from hootchunk import hooterrors

@pytest.fixture(scope="session")
def gen_file(filename='temp.txt', location='tmp', size=1048576, chunksize=999):
    file_path = '/{0}/{1}'.format(location, filename)
    if chunksize == None:
        chunksize = 10*1024*1024
    with open('/{0}/{1}'.format(location, filename), 'wb') as target:
        while size > chunksize:
            target.write(os.urandom(chunksize))
            size -= chunksize
        target.write(os.urandom(size))
    os.chmod(file_path, 744)
    return '/{0}/{1}'.format(location, filename)

@pytest.fixture(scope="session")
def return_file_key():
    returned = hootchunk.WriteToCache(gen_file)
    assert type(returned) == io.BytesIO
    return returned

def clean_file(filename, location):
    if filename in os.listdir('/{}'.format(location)):
        os.remove('/{0}/{1}'.format(location, filename))

def test_write_giant_file():
    file = '/{0}/{1}'.format('temp1.txt','tmp')
    size = 104857600
    with pytest.raises(Exception) as  excinfo:
        with open(file, 'wb') as target:
            while size > chunksize:
                target.write(os.urandom(chunksize))
                size -= chunksize
            target.write(os.urandom(104857600))

        returned = hootchunk.WriteToCache(file)
        assert 'FileError' in returned
    clean_file('temp1.txt','tmp')

def test_write_file():
    with pytest.raises(Exception) as excinfo:
        gen_file
        returned = hootchunk.WriteToCache('/tmp/temp.txt')
        if 'temp.txt' not in returned:
            assert 'KeyCollision' in str(excinfo.value)
        else:
            assert 'temp.txt' in returned
            assert 'tmp' not in returned
        clean_file('temp.txt','tmp')