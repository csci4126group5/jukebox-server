"""
API for the distributed fitness jukebox
"""
import random
import string
import os
import time
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from mutagen.mp3 import MP3

# The length of the group codes that are generated
CODE_LENGTH = 4

# The location for uploads
UPLOAD_FOLDER = '/mp3/t<device_id>'

# Which song file extensions we allow
ALLOWED_EXTENSIONS = set(['WAV', 'AIF', 'MP3', 'MID'])

# Create a new Flask app
APP = Flask(__name__)
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Memory store for the groups
GROUPS = {}

# Songs are stored in local storage, in the mp3 directory
if not os.path.exists('mp3'):
    os.makedirs('mp3')


def allowed_file(filename):
    """
    Return whether or not the file is proper
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS


def generate_group_code():
    """
    Generate an uppercase alphanumeric code, of length CODE_LENGTH
    """
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(CODE_LENGTH))


def get_device_songs(device_id):
    """
    Get the songs a device has uploaded
    """
    path = 'mp3/' + device_id
    if not os.path.exists(path):
        os.makedirs(path)

    return os.listdir(path)


def set_group_song(group_code, device_id, song_name):
    """
    Set the song for a group
    """
    start_time = time.time()
    GROUPS[group_code]['currentSong'] = {
        'url': '/' + device_id + '/mp3/' + song_name,
        'end_time': start_time + MP3('mp3/' + device_id + '/' + song_name).info.length,
    }


@APP.route('/group', methods=['GET'])
def all_groups():
    """
    List all of the groups and their playlists
    """
    return jsonify(GROUPS)


@APP.route('/group', methods=['POST'])
def create_group():
    """
    Create a new group with a random code
    """
    group_code = generate_group_code()
    while group_code in GROUPS:
        group_code = generate_group_code()
    GROUPS[group_code] = {
        'code': group_code,
        'members': [],
        'currentSong': None,
    }
    return jsonify(GROUPS[group_code])


@APP.route('/group/<group_code>', methods=['GET'])
def group_information(group_code):
    """
    Return the information for a single group
    """
    if group_code not in GROUPS:
        return 'Bad Request group code does not exist', 400

    group = GROUPS[group_code]

    # If there is a current song, and it is over, get a new one
    if group['currentSong'] and group['currentSong']['end_time'] < time.time():
        max_member = {
            'score': 0
        }
        # Find the member (with songs) with the highest score
        for member in group['members']:
            if member['score'] >= max_member['score'] and len(get_device_songs(member['device_id'])) > 0:
                max_member = member
        if max_member['device_id']:
            songs = get_device_songs(max_member['device_id'])
            if len(songs) > 0:
                random.shuffle(songs)
                song = songs.pop()
                set_group_song(group_code, max_member['device_id'], song)

    return jsonify(GROUPS[group_code])


@APP.route('/group/<group_code>', methods=['POST'])
def join_group(group_code):
    """
    Join a group with a username and device ID
    """
    if group_code not in GROUPS:
        return 'Bad Request group code does not exist', 400

    group = GROUPS[group_code]
    body = request.get_json()

    if 'name' not in body or 'device_id' not in body:
        return 'Bad Request body requires name and device_id', 400

    for member in group['members']:
        if member['device_id'] == body['device_id']:
            member['name'] = body['name']
            return jsonify(group)

    group['members'].append({
        'name': body['name'],
        'device_id': body['device_id'],
        'score': 0
    })

    # If someone joins a group and there is no song yet, grab one from their
    # list (if they have songs)
    if not group['currentSong']:
        songs = get_device_songs(body['device_id'])
        random.shuffle(songs)
        if len(songs) > 0:
            song = songs.pop()
            set_group_song(group_code, body['device_id'], song)

    return jsonify(group)


@APP.route('/group/<group_code>/member/<device_id>', methods=['PUT'])
def update_score(group_code, device_id):
    """
    Update the score for a user in a group
    """
    body = request.get_json()

    if 'score' not in body:
        return 'Bad Request body requires score', 400

    if group_code not in GROUPS:
        return 'Bad Request group code does not exist', 400

    group = GROUPS[group_code]
    for member in group['members']:
        if member['device_id'] == device_id:
            member['score'] = body['score']
            return jsonify(member)

    return 'Not Found device id does not belong to group', 404


@APP.route('/<device_id>/mp3', methods=['GET'])
def user_songs(device_id):
    """
    List all of the songs a device has uploaded
    """
    songs = get_device_songs(device_id)
    result = []
    for song in songs:
        result.append({
            'name': song,
            'url': '/' + device_id + '/mp3/' + song
        })

    return jsonify(result)


@APP.route('/<device_id>/mp3', methods=['POST'])
def uploaded_file(device_id):
    """
    Upload a song to a user's list
    """
    path = 'mp3/' + device_id
    if not os.path.exists(path):
        os.makedirs(path)

    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'Bad Request file required for upload', 400

    upload = request.files['file']

    # If user does not select file, browser submits an empty part without
    # filename
    if upload.filename == '':
        return 'Bad Request file required for upload', 400
    elif allowed_file(upload.filename):
        filename = secure_filename(upload.filename)
        upload.save(os.path.join(path, filename))

        result = {
            "name": filename,
            "url": '/' + device_id + '/mp3/' + filename
        }

        return jsonify(result)


@APP.route('/<device_id>/mp3/<song_name>', methods=['GET'])
def download_song(device_id, song_name):
    """
    Download a specified song
    """
    path = 'mp3/' + device_id
    if not os.path.exists(path):
        return 'path does not exist'

    return send_from_directory(path, song_name)


if __name__ == '__main__':
    APP.run(debug=True)
