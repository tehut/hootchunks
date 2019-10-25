
from app import app
import pytest
import sys, os, tempfile, io
# import mocker


@pytest.fixture
def client():
    app.config['TESTING'] = True
    test_client = app.test_client()

    return test_client


def test_get(client):
    resp = client.get('/hootcache/api/v1.0/files')
    assert resp.status_code == 200
    
def test_get_files(client):
    resp = client.get('/hootcache/api/v1.0/files')
    assert 'cached_files' in resp.data.decode('utf-8')

def test_post_file(client):
    with pytest.raises(Exception) as  excinfo:
        data = dict(
            file=(io.BytesIO(b'my file contents'), 'temp.txt') 
        )

        response = client.post(
        '/hootcache/api/v1.0/files/temp.txt', data=data, follow_redirects=True,
            content_type='multipart/form-data'
        )

        if 'Your item has been saved' not in response.data:
            assert 'KeyCollision' in str(excinfo.value)
        else:
            assert 'Your item has been saved' in response.data

def test_post_illegal_file(client):
    with pytest.raises(Exception) as  excinfo:
        data = dict(
            file=(io.BytesIO(b'my file contents'), 'temp.bak') 
        )

        response = client.post(
        '/hootcache/api/v1.0/files/temp.txt', data=data, follow_redirects=True,
            content_type='multipart/form-data'
        )

        assert response.status_code == 400
        


def test_get_file(client):
    resp = client.get('/hootcache/api/v1.0/files/temp.txt')
    assert 'temp.txt' in resp.data.decode('utf-8')

