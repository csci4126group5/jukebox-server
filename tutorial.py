"""
Flask API Tutorial

By Alex Lockhart and Asma Alhajri
"""

from flask import Flask, jsonify, request

APP = Flask(__name__)

GROUPS = ["Best Group", "Workout Team"]

@APP.route('/', methods=['GET'])
def get_groups():
    """
    Return the full list of groups
    """
    return jsonify(GROUPS)

@APP.route('/', methods=['POST'])
def add_group():
    """
    Add a group that has been submitted to the server
    We get the body of the request using request.data
    """
    body = request.data
    GROUPS.append(body)
    return jsonify(GROUPS)

@APP.route('/<group_number>', methods=['GET'])
def get_group(group_number):
    """
    Get a specific group at an index
    """
    index = int(group_number)
    return jsonify(GROUPS[index])

@APP.route('/<group_number>', methods=['PUT'])
def update_group(group_number):
    """
    Update a specific group at an index, and return it
    """
    index = int(group_number)
    body = request.data
    GROUPS[index] = body
    return jsonify(GROUPS[index])

@APP.route('/<group_number>', methods=['DELETE'])
def delete_group(group_number):
    """
    Delete a specific group at an index
    """
    index = int(group_number)
    GROUPS.pop(index)
    return "OK"

if __name__ == '__main__':
    APP.run(debug=True)
