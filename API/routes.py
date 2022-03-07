from API import app
from flask import jsonify
from API.mls_results import get_all_results


@app.route('/status', methods=['GET', 'POST'])
def status():
    return jsonify({'Status': 'UP'})


@app.route('/results/', methods=['GET'])
def all_results():
    return jsonify(get_all_results())
