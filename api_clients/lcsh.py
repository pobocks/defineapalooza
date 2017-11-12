from .common import *
from lxml.etree import iterparse

SUBJECT_Q = "cs:http://id.loc.gov/authorities/subjects"
XHTML_NS = "{http://www.w3.org/1999/xhtml}"

@attr.s(slots=True)
class LCSHClient:

    # note, trailing slash is NECESSARY
    base = attr.ib(default="http://id.loc.gov/search/")
    entries_base = attr.ib(default="http://id.loc.gov{}.json")
    session = attr.ib(default=Factory(FSFactory))

    def search_request(self, word:str, background_callback=None):
        return self.session.get(self.base,
                                params = {"q": [word.lower(),
                                                SUBJECT_Q]},
                                stream=True,
                                background_callback=background_callback)

    def entries_hook(self, sesh, resp, *args, **kwargs):
        '''Callback that processes XHTML response, pulls out actionable links to LOC subject entries, and batches requests for them.'''
        results = {}
        if resp.status_code == 200:
            for _, element in iterparse(resp.raw, tag="{}a".format(XHTML_NS)):
                if element.attrib.get('href', '').startswith('/authorities/subjects'):
                    results[element.text] = self.entries_base.format(element.attrib['href'])
                    element.clear()
            if len(results) > 0:
                resp.callback_result = results
            else:
                resp.callback_result = False

    def __call__(self, word:str):
        '''Convenience method to search for a word and return all JSON responses.'''
        final_result = self.search_request(word, background_callback = self.entries_hook)

        def output():
            return final_result.result().callback_result

        return self.session.executor.submit(output)
