from .common import app, betamax

from api_clients import OxfordClient, LCSHClient

@betamax.use_cassette
def test_oxford_client():
    '''Smoke test for Oxford Dictionary API Client'''
    with app.application.app_context():
        oxford = OxfordClient()
        future = oxford('test')
        assert future.result
        assert future.result()
