from API import app
from API.mls_results import get_all_results


@app.route('/status/', methods=['GET', 'POST'])
def status():
    return {'Status': 'UP'}


@app.route('/results/', methods=['GET'])
def all_results():
    return get_all_results()


@app.route('/results/<team_code>', methods=['GET'])
def team_results(team_code):
    return get_all_results(team=team_code.upper())


@app.route('/results/<team_code>/<year>', methods=['GET'])
def team_results_by_year(year, team_code):
    return get_all_results(years=[year], team=team_code.upper())
