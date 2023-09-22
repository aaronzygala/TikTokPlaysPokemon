from flask import Flask, jsonify, request, abort
import math
import logging
from threading import Thread
logging.basicConfig(level=logging.DEBUG, filename="output.log")  # Set the desired log level

ADMIN_USER = {
    'username': 'admin',
    'password': 'password'
}
app = Flask(__name__)
# app.config['SECRET_KEY'] = "skM0gRq7zxJyaLQkApKyi49d2x9Uq8Ug"

@app.route('/api/login', methods=['POST'])
def login():
    app.logger.debug("Received login request")

    # Logging request data
    app.logger.debug(f"Request form data: {request}")
    data = request.json
    submitted_username = data.get('username')
    submitted_password = data.get('password')
    app.logger.debug(f"Submitted username: {submitted_username}")
    app.logger.debug(f"Submitted password: {submitted_password}")
    if submitted_username == ADMIN_USER['username'] and submitted_password == ADMIN_USER['password']:
        response = jsonify({'message': 'Login successful'})
        return response
    else:
        return abort(401)

# Define a global variable to hold the live_manager object
live_manager = None

@app.route('/api/recent_comments', methods=['GET'])
def get_recent_comments():
    if live_manager is not None:
        page = request.args.get("page", type=int, default=1)
        pageSize = request.args.get("pageSize", type=int, default=8)

        comments = live_manager.get_recent_comments()

        # Calculate the total number of pages using math.ceil
        max_pages = math.ceil(len(comments) / pageSize)

        # Calculate the start and end indices for the comments to return
        start_index = (page - 1) * pageSize
        end_index = start_index + pageSize

        # Get a subset of recent comments based on pagination
        paginated_comments = comments[start_index:end_index]

        # Create a dictionary containing recent comments and maxPages
        data = {
            'recentComments': paginated_comments,
            'maxPages': max_pages
        }

        return jsonify(data), 200
    else:
        return jsonify([]), 200  # Return an empty response if live_manager is None

def get_names_from_file(file_path):
    try:
        # Read names from the specified file
        with open(file_path, 'r') as file:
            names = [line.strip() for line in file if line.strip()]  # Exclude empty lines

        # Create a JSON object containing the names
        data = {'names': names}

        return data, 200
    except Exception as e:
        return {'error': str(e)}, 500

def add_name():
    data = request.get_json()
    name = data.get('name')
    if name:
        names.append(name)
        return jsonify({'message': 'Name added successfully'})
    else:
        return jsonify({'error': 'Name cannot be empty'})

@app.route('/api/whitelist', methods=['GET'])
def get_whitelist():
    data, status_code = get_names_from_file('./users/whitelist.txt')
    return jsonify(data), status_code
@app.route('/api/whitelist/add', methods=['POST'])
def add_to_whitelist():
    data = request.get_json()
    name = data.get('name')
    if name:
        live_manager.whitelist_user(name)
        return jsonify({'message': 'Name added successfully'})
    else:
        return jsonify({'error': 'Name cannot be empty'})
@app.route('/api/whitelist/remove', methods=['POST'])
def remove_from_whitelist():
    data = request.get_json()
    name = data.get('name')
    if name:
        live_manager.remove_from_whitelist(name)
        return jsonify({'message': 'Name removed successfully'})
    else:
        return jsonify({'error': 'Name not found in the list'})

@app.route('/api/banned', methods=['GET'])
def get_banned_list():
    data, status_code = get_names_from_file('./users/banned.txt')
    return jsonify(data), status_code

@app.route('/api/banned/add', methods=['POST'])
def add_to_banned_list():
    data = request.get_json()
    name = data.get('name')
    if name:
        live_manager.ban_user(name, "baz4k")
        return jsonify({'message': 'Name added successfully'})
    else:
        return jsonify({'error': 'Name cannot be empty'})
@app.route('/api/banned/remove', methods=['POST'])
def remove_from_banned_list():
    data = request.get_json()
    name = data.get('name')
    if name:
        live_manager.remove_from_banned_list(name)
        return jsonify({'message': 'Name removed successfully'})
    else:
        return jsonify({'error': 'Name not found in the list'})

@app.route('/api/admins', methods=['GET'])
def get_admins():
    data, status_code = get_names_from_file('./users/admin.txt')
    return jsonify(data), status_code

@app.route('/api/admins/add', methods=['POST'])
def add_to_admins():
    data = request.get_json()
    name = data.get('name')
    if name:
        live_manager.admin_user(name)
        return jsonify({'message': 'Name added successfully'})
    else:
        return jsonify({'error': 'Name cannot be empty'})
@app.route('/api/admins/remove', methods=['POST'])
def remove_from_admins():
    data = request.get_json()
    name = data.get('name')
    if name:
        live_manager.remove_from_admin(name)
        return jsonify({'message': 'Name removed successfully'})
    else:
        return jsonify({'error': 'Name not found in the list'})
@app.route('/api/toggle_mode', methods=['POST'])
def toggle_mode():
    if live_manager is not None:
        mode = live_manager.toggle_mode()

        # Create a dictionary containing recent comments and maxPages
        data = {
            'mode': mode,
        }

        return jsonify(data), 200
    else:
        return jsonify(''), 200  # Return an empty response if live_manager is None

def get_statistic(stat_name):
    if live_manager is not None:
        if stat_name == "followers":
            stat = live_manager.get_follow_count()
        elif stat_name == "comments":
            stat = live_manager.get_comment_count()
        else:
            stat = live_manager.get_viewer_count()
        # Create a dictionary containing recent comments and maxPages
        data = {
            'stat': stat,
        }

        return jsonify(data), 200
    else:
        return jsonify(''), 200  # Return an empty response if live_manager is None

@app.route('/api/followers', methods=['GET'])
def get_followers():
    data, status_code = get_statistic('followers')
    return data, status_code

@app.route('/api/comments', methods=['GET'])
def get_comments():
    data, status_code = get_statistic('comments')
    return data, status_code

@app.route('/api/viewers', methods=['GET'])
def get_viewers():
    data, status_code = get_statistic('viewers')
    return data, status_code

def run_flask_app():
    app.run(debug=True, port=5002, use_reloader=False)
def run_flask_thread():
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

if __name__ == '__main__':
    run_flask_app()

