from API import app
from flask import jsonify


@app.route('/status', methods=['GET', 'POST'])
def status():
    return jsonify({'Status': 'UP'})
