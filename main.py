# -*- coding: utf-8 -*-
#
# (c) 2017 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
"""
Serve static files from an S3 private bucket (it does not need to be
set up as a website)
Author: Alessandro Pasotti
"""
import os
from flask import Flask, make_response, abort, render_template
from simples3 import S3Bucket, KeyNotFound

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))

app = Flask(__name__)

bucket = S3Bucket(os.getenv("S3_BUCKET_NAME"),
                  os.getenv("AWS_ACCESS_KEY"),
                  os.getenv("AWS_SECRET_KEY"))

def try_file(path):
    """Serve the file if it does exist, raise KeyNotFound if not"""
    f = bucket.get(path)
    if f.s3_info["size"] == 0: # It's a directory!
        raise KeyNotFound("Not a file")
    content_type = f.s3_info["mimetype"]
    response = make_response(f.read())
    response.headers['Content-Type'] = content_type
    if not content_type.startswith('text/') and not content_type.startswith('image/'):
        response.headers['Content-Disposition'] = \
            'inline; filename=%s' % (path[path.rfind('/')] if path.find('/') != -1 else path)
    response.headers['Last-Modified'] = f.s3_info["modify"].isoformat()
    return response


@app.route('/', methods=['GET'])
def index(path=''):
    """Serve index.html or a directory listing"""
    try:
        return try_file('%sindex.html' % path)
    except KeyError as e:
        pass
    # Directory listing
    # Make sure the path is ending with a slash if not empty
    if path and not path.endswith('/'):
        path = path + '/'
    items = []
    for (key, modify, etag, size) in bucket.listdir(path):
        href = key
        key = key[len(path):]
        slash_count = key.count('/')
        # Skip sub directories and files in sub-directories
        if key and (slash_count == 0 or (slash_count == 1 and key[-1] == '/')):
            items.append({
            'key': key,
            'href': '/' + href,
            'etag': etag,
            'size': size,
            'modify': modify
            })
    if not len(items):
        abort(404)
    # Get parent
    parent = '/' + '/'.join([p for p in path.split('/') if p][:-1])
    if parent == path:
        parent = None
    # Add slash
    path = '/' + path
    return render_template('index.html', items=items, path=path, parent=parent)


@app.route('/<path:path>', methods=['GET'])
def bridge(path):
    try:
        return try_file(path)
    except KeyNotFound as e:
        return index(path)


if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)
