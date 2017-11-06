import flask
from flask import g, Blueprint, render_template, request, Response, abort
from flask.json import jsonify

import json
api = Blueprint('api_v1', __name__, template_folder='templates')

@api.route('/', methods=['GET'])
def index():
    return json.dumps([(str(rule.methods), rule.rule, rule.endpoint,)
                       for rule
                       in flask.current_app.url_map.iter_rules()
                       if rule.endpoint.startswith(api.name + '.')]
    )

@api.route('/word/<word>', methods=['GET'])
def word(word):
    if not word:
        abort(404)
    else:
        c = flask.current_app.get_oxford_client()
        return Response(c(word.lower()).result().content, mimetype="application/json")
