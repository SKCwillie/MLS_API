from MLS_API.API import app


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>This is the start</h1>'
