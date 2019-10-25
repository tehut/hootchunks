# import pytest

# @pytest.fixture(scope="session")
# def gen_file(filename='temp.txt', location='tmp', size=1048576, chunksize=999):
#     if chunksize == None:
#         chunksize = 10*1024*1024
#     # file=(io.BytesIO(os.urandom(chunksize)), 'temp.txt') 
#     with open('/{0}/{1}'.format(location, filename), 'wb') as target:
#         while size > chunksize:
#             target.write(os.urandom(chunksize))
#             size -= chunksize
#         target.write(os.urandom(size))
#     return '/{0}/{1}'.format(location, filename)

# @pytest.fixture(scope="session")
# def return_file_key():
#     file_loc = gen_file
#     returned = hootchunk.ReadFromCache(file_loc)
#     assert type(returned) io.BytesIO