import attr
from attr import Factory
from requests_futures.sessions import FuturesSession

from flask import current_app

def FSFactory():
    s = FuturesSession(max_workers=4)
    s.headers.update(current_app.config['OXFORD_API_INFO'])
    return s
