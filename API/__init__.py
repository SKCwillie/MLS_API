from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('MLS_API_KEY')

from MLS_API.API import routes