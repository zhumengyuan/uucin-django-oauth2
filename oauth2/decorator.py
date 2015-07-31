# encoding:utf-8


import re
from django.http.response import HttpResponseForbidden
from oauth2.passport import get_token_userid


def token_required(view, required=True):
    def decorator(request, *args, **kwargs):
        request.access_token = None
        request.uucode = None
        try:
            request.access_token = re.match(
                '^token (\w+)', request.META['HTTP_AUTHORIZATION']).groups()[0]
        except (KeyError, AttributeError):
            pass
        request.uucode = get_token_userid(request.access_token)
        if required:
            return HttpResponseForbidden()
        return view(request, *args, **kwargs)
    return decorator
