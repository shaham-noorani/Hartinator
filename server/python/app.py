from flask import Flask, jsonify, request
from flask_cors import CORS
from hartinator import PartWriter

# configuration
DEBUG = True
VOICES = ["lmao"]

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('lmap!')

# return notes 
@app.route('/notes', methods=['POST', 'GET'])
def respondWithNotes():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        progression = post_data.get('progression')
        key = post_data.get('key')
        PartWriterImpl = PartWriter(key, progression)
        PartWriterImpl.writeBassLine()
        PartWriterImpl.writeLine()
        VOICES.append(PartWriterImpl.voices)
    else:
        response_object['voices'] = VOICES[-1]
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()