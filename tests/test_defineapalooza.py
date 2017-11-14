from .common import app, betamax
from lxml.etree import fromstring, HTMLParser

parser = HTMLParser()

@betamax.use_cassette
def test_root():
    '''Smoke test for "does the app even route?"'''
    rv = app.get('/')
    assert rv.status_code == 200

@betamax.use_cassette
def test_search():
    page = fromstring(app.get('/').data, parser=parser)
    csrf = page.find('.//input[@id="csrf_token"]').attrib['value']

    rv = app.post('/', data={"word": "test", "csrf_token": csrf})
    assert rv.status_code == 200
    assert 'a procedure intended to establish the quality, performance, or reliability of something, especially before it is taken into widespread use' in str(rv.data, 'utf-8')
    assert 'National Merit Scholarship Qualifying Test' in str(rv.data, 'utf-8')


@betamax.use_cassette
def test_docs():
    '''Smoke test for /docs/ route'''
    rv = app.get('/docs')
    assert rv.status_code == 301

    rv = app.get('/docs/')
    assert rv.status_code == 200
