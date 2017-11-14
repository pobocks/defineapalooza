from .common import app, betamax
import json
from lxml.etree import fromstring, HTMLParser

parser = HTMLParser()

@betamax.use_cassette
def test_word():
    rv = app.get('/api/v1/word/test', headers={"accept": "application/json"})
    assert json.loads(rv.data)

def test_word_fragment():
    rv = app.get('/api/v1/word/test', headers={"accept": "text/html"})
    html = fromstring(rv.data, parser=parser)
    assert len(html.xpath('//div[starts-with(@class, "lexical-entry")]')) > 0
