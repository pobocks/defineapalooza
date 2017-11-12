import flask
from flask import g, Blueprint, render_template, request, Response, abort
from flask.json import jsonify

import json
api = Blueprint('api_v1', __name__, template_folder='templates')

@api.route('/', methods=['GET'])
def index():
    '''Return list of routes and endpoints'''
    return json.dumps([(str(rule.methods), rule.rule, rule.endpoint,)
                       for rule
                       in flask.current_app.url_map.iter_rules()
                       if rule.endpoint.startswith(api.name + '.')]
    )

@api.route('/word/<word>', methods=['GET'])
def word(word):
    '''Return either JSON or HTML representation of a definition'''
    if not word:
        abort(404)
    else:
        c = flask.current_app.get_oxford_client()
        res = c(word.lower()).result()
        if "application/json" in request.accept_mimetypes:
            return Response(res.content, mimetype="application/json")
        else:
            return Response(render_template('api/lex_entry_fragment.html', entries=res.json()['results'][0]['lexicalEntries']), mimetype='text/html')
