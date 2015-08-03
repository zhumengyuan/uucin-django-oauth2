# encoding:utf-8


import json
import requests
from django.conf import settings
from django.core.cache import cache


UUCIN_OAUTH2_DOMAIN = getattr(
    settings, 'UUCIN_OAUTH2_DOMAIN', 'https://passport.uucin.com')
UUCIN_OAUTH2_TOKEN_CACHE = getattr(
    settings, 'UUCIN_OAUTH2_TOKEN_CACHE', ('uucin_oauth2_token', 60 * 5))


def get_token_userid(access_token):
    if not access_token:
        return
    result = cache.get('%s:%s' % (UUCIN_OAUTH2_TOKEN_CACHE[0], access_token))
    if result:
        return json.loads(result)['userid']
    resp = requests.get(
        '%s/oauth/2.0/token/info' % UUCIN_OAUTH2_DOMAIN,
        headers={'Authorization': 'token %s' % access_token})
    if resp.status_code == 200:
        result = json.loads(resp.content)
        cache.set(
            '%s:%s' % (UUCIN_OAUTH2_TOKEN_CACHE[0], access_token),
            json.dumps(result, ensure_ascii=False),
            UUCIN_OAUTH2_TOKEN_CACHE[1])
        return result['userid']
