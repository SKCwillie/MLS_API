from MLS_API.API import app
from flask import jsonify


@app.route('/status', methods=['GET', 'POST'])
def home():
    return jsonify({'Status': 'UP'})
