from flask import Flask, g, request, send_from_directory, render_template
import os
app = Flask(__name__)

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

