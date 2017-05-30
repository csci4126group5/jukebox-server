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

def generate_group_code():
    """
    Generate an uppercase alphanumeric code, of length CODE_LENGTH
    """
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(CODE_LENGTH))

def generate_group_schema(group_code):
    """
    For a given group, return what songs are ready to play and which haven't been uploaded
    """
    return {
        'code': group_code,
        'playlist': [f for f in os.listdir('mp3') if f in GROUPS[group_code]],
        'unavailable': [f for f in os.listdir('mp3') if f not in GROUPS[group_code]]
    }

@APP.route('/mp3', methods=['GET'])
def all_files():
    """
    List all of the songs in the mp3 directory, where they are stored
    """
    if not os.path.exists('mp3'):
        os.makedirs('mp3')
    return jsonify(os.listdir('mp3'))

@APP.route('/group', methods=['GET'])
def all_groups():
    """
    List all of the groups and their playlists
    """
    return jsonify([generate_group_schema(group_code) for group_code in GROUPS])

@APP.route('/group', methods=['POST'])
def create_group():
    """
    Create a new group with a random code
    """
    group_code = generate_group_code()
    while group_code in GROUPS:
        group_code = generate_group_code()
    GROUPS[group_code] = []
    return jsonify(generate_group_schema(group_code))

@APP.route('/group/<group_code>', methods=['GET'])
def group_files(group_code):
    """
    Return the information for a single group
    """
    if group_code not in GROUPS:
        return 'Bad Request group code does not exist', 400
    return jsonify(generate_group_schema(group_code))

if __name__ == '__main__':
    APP.run(debug=True)
