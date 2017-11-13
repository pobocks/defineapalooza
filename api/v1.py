import flask
from flask import g, Blueprint, render_template, request, Response, abort
from flask.json import jsonify

import json
api = Blueprint('api_v1', __name__, template_folder='templates')

@api.route('/', methods=['GET'])
def index():
    '''Return list of routes and endpoints.'''
    return json.dumps([(str(rule.methods), rule.rule, rule.endpoint,)
                       for rule
                       in flask.current_app.url_map.iter_rules()
                       if rule.endpoint.startswith(api.name + '.')]
    )

@api.route('/word/<word>', methods=['GET'])
def word(word):
    '''Return either JSON or HTML representation of definitions and LCSH search results for a word.'''
    if not word:
        abort(404)
    else:
        oxford = flask.current_app.get_oxford_client()
        lcsh = flask.current_app.get_lcsh_client()
        oxford_fut, lcsh_fut = (oxford(word.lower()), lcsh(word.lower()),)
        
        if "application/json" in request.accept_mimetypes:
            return jsonify({"oxford": oxford_fut.result(),
                            "lcsh": lcsh_fut.result()})
        else:
            return Response(render_template('api/lex_entry_fragment.html', data=oxford_fut.result(), lcsh_data=lcsh_fut.result(), mimetype='text/html'))
