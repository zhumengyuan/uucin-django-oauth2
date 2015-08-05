# encoding:utf-8


import re
import json
from django.http.response import HttpResponseForbidden, HttpResponseBadRequest
from oauth2.passport import get_token_userid


def token_required(view, required=True, json_stream=True, has_version=True):
    def decorator(request, *args, **kwargs):
        try:
            request.access_token = re.match(
                '^token (\w+)', request.META['HTTP_AUTHORIZATION']).groups()[0]
        except (KeyError, AttributeError):
            request.access_token = None
        request.uucode = get_token_userid(request.access_token)
        if required and not request.uucode:
            return HttpResponseForbidden()
        if json_stream and request.method in ['PUT', 'POST', 'PATCH']:
            stream = request.body
            if stream:
                try:
                    request.jsondata = json.loads(stream)
                except ValueError:
                    return HttpResponseBadRequest(json.dumps({
                        "message": "Problems parsing JSON"}))
        if has_version:
            try:
                request.version = re.match(
                    '^application/vnd.uucin.v(.+)\+json',
                    request.META['HTTP_ACCEPT']).groups()[0]
            except (KeyError, AttributeError):
                request.version = None
        return view(request, *args, **kwargs)
    return decorator
