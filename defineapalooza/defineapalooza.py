from flask import Flask, g, request, send_from_directory, render_template

from flask_bootstrap import Bootstrap

# Note: shorthanding n?gettext
from flask_babel import Babel, gettext as gt, ngettext as gts

from flask_wtf import FlaskForm as Form
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os

from api_clients import OxfordClient, LCSHClient
from api import api

from concurrent.futures import as_completed



app = Flask(__name__,
            instance_relative_config=True,
            instance_path=os.path.abspath('./instance'))

app.register_blueprint(api, url_prefix="/api/v1")
app.config.from_object('config.default')
app.config.from_pyfile('application.cfg', silent=True)

bootstrap = Bootstrap(app)
csrf = CsrfProtect(app)
babel = Babel(app)

def get_oxford_client():
    if not hasattr(g, 'oxford_client'):
        g.oxford_client = OxfordClient()
    return g.oxford_client

def get_lcsh_client():
    if not hasattr(g, 'lcsh_client'):
        g.lcsh_client = LCSHClient()
    return g.lcsh_client

app.get_oxford_client = get_oxford_client
app.get_lcsh_client = get_lcsh_client

# Form
class WordForm(Form):
    word = StringField("Word to Look Up", validators=[DataRequired()],
                       render_kw={'placeholder': 'Look up...'})
    submit = SubmitField('Submit') # Not used currently, but completion sake

# Routes

@app.route("/")
def home():
    '''Our glorious homepage, reknowned in story and song!'''
    return render_template('index.html', word_form=WordForm())

@app.route("/", methods=["POST"])
def fetch_word():
    '''Action for the index page form (in absence of JS). Also contains form.'''
    oxford = get_oxford_client()
    lcsh = get_lcsh_client()
    word = request.form['word']

    data = oxford(word)
    lcsh_data = lcsh(word)
    return render_template('fetch.html',
                           word=word,
                           data=data.result() or [],
                           lcsh_data=lcsh_data.result() or {},
                           word_form=WordForm())


@app.route('/docs/', defaults={'filename': 'index.html'})
@app.route('/docs/<path:filename>')
def documentation(filename):
    '''Return this fine documentation'''
    return send_from_directory(
        os.path.abspath('./docs/_build/html'),
        filename
    )
