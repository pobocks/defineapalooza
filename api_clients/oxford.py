from .common import *

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
        def failure():
            return False
        
        if resp.status_code == 200:
            try:
                resp.callback_result = self.definition_request(resp.json()['results'][0]['id'])
            except (IndexError, KeyError):
                resp.callback_result = self.session.executor.submit(failure)

    def __call__(self, word:str):
        '''Convenience method to search for a word and return the first search result'''
        final_result = self.search_request(word, background_callback = self.def_request_hook)

        def output():
            res = final_result.result()
            
            try:
                return res.callback_result.result().json()['results'][0]['lexicalEntries']
            except:
                return False
            
        return self.session.executor.submit(output)
