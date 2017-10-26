import defineapalooza

app = defineapalooza.app.test_client()

def test_root():
    '''Smoke test for "does the app even route?"'''
    rv = app.get('/')
    assert rv.status_code == 200

def test_docs():
    '''Smoke test for /docs/ route'''
    rv = app.get('/docs')
    assert rv.status_code == 301
    
    rv = app.get('/docs/')
    assert rv.status_code == 200
