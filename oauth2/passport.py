# encoding:utf-8


import json
import requests
from django.conf import settings


UUCIN_OAUTH2_DOMAIN = getattr(
    settings, 'UUCIN_OAUTH2_DOMAIN', 'https://passport.uucin.com')


def get_token_userid(access_token):
    if not access_token:
        return
    resp = requests.get(
        '%s/oauth/2.0/token/info' % UUCIN_OAUTH2_DOMAIN,
        headers={'Authorization': 'token %s' % access_token})
    if resp.status_code == 200:
        return json.loads(resp.content)['userid']
