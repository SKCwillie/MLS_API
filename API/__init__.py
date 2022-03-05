import Flask
import os

app = Flask(__name__)
app.config = os.environ['MLS_API_KEY']

from MLS_API import routes
