#!flask/bin/python
import os, io, sys, atexit
from hootchunk import hootchunk 

from flask import Flask, jsonify, abort, make_response, request
from werkzeug.utils import secure_filename


if len(sys.argv) > 1:
    SERVICEIP = sys.argv[1]
else:
    raise Error("Restart service with Cache Service IP address as parameter.  Ex:  python3 app.py $serviceIP")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
app.config['DEBUG'] = 'FALSE'
base_url = '/hootcache/api/v1.0/'

cached_files = []

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/hootcache/api/v1.0/files', methods=['GET'])
def get_files():
    return jsonify({'cached_files': cached_files})

@app.route('/hootcache/api/v1.0/files/<file_name>', methods=['GET'])
def get_file(file_name):
    file = [file for file in cached_files if file['file_name'] == file_name ]
    file_body = hootchunk.ReadFromCache(file_name)
    new = file_body.decode('UTF-8')
    return jsonify({'meta_data':file_name,'body': new})

@app.route('/hootcache/api/v1.0/files/<file_name>', methods=['POST'])
def upload_file(file_name):
    safe =  '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    file = request.files['file']

    if 'file' not in request.files:
        resp = jsonify({'message': 'No file found in request'})
    if file_name == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and safe:
        filename = secure_filename(file_name)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cache_response = hootchunk.WriteToCache(file_path)
        if filename in cache_response:
            cached_files.append({'cache_key': cache_response, 'file_name': filename})
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        print(cached_files)
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif, csv, dat'})
        resp.status_code = 400
    return resp


atexit.register(hootchunk.FlushCache)

if __name__ == '__main__':
    app.run(debug=True)


