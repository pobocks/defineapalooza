import attr
from attr import Factory
from requests_futures.sessions import FuturesSession
from flask import current_app

def FSFactory():
    s = FuturesSession(max_workers=2)
    s.headers.update(current_app.config['OXFORD_API_INFO'])
    return s

@attr.s(slots=True)
class result:
    future = attr.ib()

    def result(self):
        sub_future = self.future.result().callback_future
        if sub_future:
            return sub_future.result()

@attr.s(slots=True)
class OxfordClient:
    headers = attr.ib(default=Factory(dict))
    base = attr.ib(default="https://od-api.oxforddictionaries.com/api/v1")
    session = attr.ib(default=Factory(FSFactory))

    def search_request(self, word:str, background_callback=None):
        return self.session.get("/".join((self.base, 'search', 'en',)),
                                params = {'q': word.lower()},
                                background_callback=background_callback)

    def definition_request(self, word_id:str):
        return self.session.get("/".join((self.base, 'entries', 'en', word_id,)),)

# from itertools import repeat;from api_clients import OxfordClient;c = OxfordClient()

    def def_request_hook(self, sesh, resp, *args, **kwargs):
        '''Callback that queues request for word data for first search result, storing it in data property of response'''
        if resp.status_code == 200:
            try:
                resp.callback_future = self.definition_request(resp.json()['results'][0]['id'])
            except (IndexError, KeyError):
                resp.callback_future = False

    def __call__(self, word:str):
        '''Convenience method to search for a word and return the first search result'''
        final_result = self.search_request(word, background_callback = self.def_request_hook)

        return result(final_result)
