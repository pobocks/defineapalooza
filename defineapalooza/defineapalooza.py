from flask import Flask, g, request, send_from_directory, render_template
import os

from api_clients.oxford import OxfordClient

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')
app.config.from_pyfile('application.cfg', silent=True)

@app.route("/")
def home():
    '''Our glorious homepage, reknowned in story and song!'''
    return render_template('index.html')

@app.route('/docs/', defaults={'filename': 'index.html'})
@app.route('/docs/<path:filename>')
def documentation(filename):
    '''Return this fine documentation'''
    return send_from_directory(
        os.path.abspath('./docs/_build/html'),
        filename
    )

