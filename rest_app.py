#!/usr/bin/env python

from flask import Flask, request, jsonify
from keycolumnvalue import KeyColumnValueStore

app = Flask(__name__)

db = KeyColumnValueStore(path='sample.db')


@app.route('/api/v1/keys', methods=['GET'])
def get_keys():

    """ return list of keys """

    return jsonify({'keys': db.get_keys()})


@app.route('/api/v1/keys/<key>', methods=['GET', 'DELETE'])
@app.route('/api/v1/keys/<key>/<col>', methods=['GET', 'POST', 'DELETE'])
def key(key, col=None):

    """
    GET: return list of col/vals or just vals if only col provided
    POST: insert or overwrite a new col/val and return result
    DELETE: delete col/val or entire key

    """

    if col:

        if request.method == 'DELETE':

            db.delete(key, col)

            return jsonify({'status': 'ok'})

        if request.method == 'POST':

            val = request.form.get('val')
            db.set(key, col, val)

        return jsonify({'val': db.get(key, col)})

    else:

        if request.method == 'DELETE':

            db.delete_key(key)

            return jsonify({'status': 'ok'})

        return jsonify({'columns': db.get_key(key)})


@app.route('/api/v1/keys/<key>/slice', methods=['GET'])
def slice(key):

    """ return slice of column values """

    start = request.args.get('start')
    stop = request.args.get('stop')

    return jsonify({'columns_sliced': db.get_slice(key, start, stop)})


if __name__ == '__main__':

    app.run(debug=True)
