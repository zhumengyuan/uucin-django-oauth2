# encoding:utf-8


import json
import requests
from django.conf import settings
from django.core.cache import cache


UUCIN_OAUTH2_DOMAIN = getattr(
    settings, 'UUCIN_OAUTH2_DOMAIN', 'https://passport.uucin.com')
UUCIN_OAUTH2_TOKEN_CACHE = getattr(
    settings, 'UUCIN_OAUTH2_TOKEN_CACHE', ('uucin_oauth2_token', 60 * 5))

UUCIN_OAUTH2_CLIENT_CACHE = getattr(
    settings, 'UUCIN_OAUTH2_CLIENT_CACHE', ('uucin_oauth2_client', 60 * 5))


def clean_client_data(uucode, client_id, access_token):
    key = '%s:%s:%s' % (UUCIN_OAUTH2_CLIENT_CACHE[0], uucode, client_id)
    old_token = cache.get(key)
    if old_token:
        cache.delete('%s:%s' % (UUCIN_OAUTH2_TOKEN_CACHE[0], old_token))
    cache.set(key, access_token, UUCIN_OAUTH2_CLIENT_CACHE[1])


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

        clean_client_data(result['userid'], result['client_id'], access_token)

        cache.set(
            '%s:%s' % (UUCIN_OAUTH2_TOKEN_CACHE[0], access_token),
            json.dumps(result, ensure_ascii=False),
            UUCIN_OAUTH2_TOKEN_CACHE[1])
        return result['userid']
