"""
Flask API Tutorial

By Alex Lockhart and Asma Alhajri
"""

# Step 1
from flask import Flask, jsonify, request

# Step 1
APP = Flask(__name__)

# Step 1
GROUPS = ["Best Group", "Workout Team"]

# Step 1
@APP.route('/', methods=['GET'])
def get_groups():
    """
    Return the full list of groups
    """
    return jsonify(GROUPS)

# Step 2
@APP.route('/', methods=['POST'])
def add_group():
    """
    Add a group that has been submitted to the server
    We get the body of the request using request.data
    """
    body = request.data
    GROUPS.append(body)
    return jsonify(GROUPS)

# Step 3
@APP.route('/<group_number>', methods=['GET'])
def get_group(group_number):
    """
    Get a specific group at an index
    """
    index = int(group_number)
    return jsonify(GROUPS[index])

# Step 4
@APP.route('/<group_number>', methods=['PUT'])
def update_group(group_number):
    """
    Update a specific group at an index, and return it
    """
    index = int(group_number)
    body = request.data
    GROUPS[index] = body
    return jsonify(GROUPS[index])

# Step 4
@APP.route('/<group_number>', methods=['DELETE'])
def delete_group(group_number):
    """
    Delete a specific group at an index
    """
    index = int(group_number)
    GROUPS.pop(index)
    return "OK"

# Step 1
if __name__ == '__main__':
    APP.run(debug=True)
