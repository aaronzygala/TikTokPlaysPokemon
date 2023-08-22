from flask import Flask, jsonify, request, abort
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
        comments = live_manager.get_recent_comments()
        return jsonify(comments)
    else:
        return jsonify([])

def run_flask_app():
    app.run(debug=True, port=5002, use_reloader=False)
def run_flask_thread():
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

if __name__ == '__main__':
    run_flask_app()

