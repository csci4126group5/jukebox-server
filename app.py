"""
API for the distributed fitness jukebox
"""
import random
import string
import os
from flask import Flask, jsonify

CODE_LENGTH = 4

APP = Flask(__name__)

GROUPS = {}

if not os.path.exists('mp3'):
    os.makedirs('mp3')


def generate_group_code():
    """
    Generate an uppercase alphanumeric code, of length CODE_LENGTH
    """
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(CODE_LENGTH))


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
        'nextSong': None,
    }
    return jsonify(GROUPS[group_code])


@APP.route('/group/<group_code>', methods=['GET'])
def group_information(group_code):
    """
    Return the information for a single group
    """
    if group_code not in GROUPS:
        return 'Bad Request group code does not exist', 400
    return jsonify(GROUPS[group_code])


@APP.route('/group/<group_code>', methods=['POST'])
def join_group(group_code):
    """
    TODO: Join a group with a username and device ID
    """
    pass


@APP.route('/group/<group_code>/member/<device_id>', methods=['PUT'])
def update_score(group_code, device_id):
    """
    TODO: Update the score for a user in a group
    """
    pass


@APP.route('/<device_id>/mp3', methods=['GET'])
def user_songs(device_id):
    """
    List all of the songs a device has uploaded
    """
    pass


@APP.route('/<device_id>/mp3', methods=['POST'])
def upload_song(device_id):
    """
    Upload a song to a user's list
    """
    pass


@APP.route('/<device_id>/mp3/<song_name>', methods=['GET'])
def download_song(device_id, song_name):
    """
    Download a specified song
    """
    pass


if __name__ == '__main__':
    APP.run(debug=True)
