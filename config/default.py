from os import environ as env
# Oxford ID/Key
OXFORD_API_INFO = {
    'app_id': env.get('OXFORD_APP_ID'),
    'app_key': env.get('OXFORD_APP_KEY')
}

SECRET_KEY="balderdash_changme_notforprod"
