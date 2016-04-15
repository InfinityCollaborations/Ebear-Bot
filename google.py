#!/usr/bin/env python3

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
import json


def search(query):
    #NB. add 'start=3' to the query string to move to later results
    enquery = urlencode({'q': query})
    http = Request('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + enquery)
    r = urlopen(http)
    encoding = r.headers.get_content_charset()
    theObject = json.loads(r.read().decode(encoding))
    resl = ''

    for index,result in enumerate(theObject['responseData']['results']):
        resl += ((str(index+1) + ") " + result['titleNoFormatting']))
        resl += ': '
        resl += ((result['url']))
        resl += '\n'

    return resl
