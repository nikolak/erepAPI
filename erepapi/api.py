# Copyright (c) 2013 Nikola Kovacevic   <nikolak@outlook.com>,

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# SOFTWARE

import hmac
import json
from hashlib import sha256
from sys import version_info
from time import strftime, gmtime

try:
    # Python 2
    from urllib2 import urlopen, Request
except ImportError:
    # Python 3
    from urllib.request import urlopen, Request


api_url = "http://api.erepublik.com/"
public_key = None
private_key = None


def _construct_url(resource, action, params=None):
    """
    Constructs rest of API url based on resource, action and parameters.

    Multiple parameters must be a list.

    Single parameters must be a single string

    Internal usage
    """
    final_url = '{}/{}'.format(resource, action)
    if type(params) == list:
        final_url += '?'
        for i in range(len(params)):
            if i < len(params) - 1:
                final_url += params[i] + '&'
            else:
                final_url += params[i]
    elif type(params) == str:
        final_url += '?{}'.format(params)
    else:
        pass
    return final_url



def _construct_headers(url):
    """
    Constructs headers to send with request.
    Internal usage.

    The Date header needs to be the current date and
    time of the request in RFC1123 format (e.g. Tue, 04 Sep 2012 15:57:48)

    The Auth header structure is {public_key}/{digest} where {public_key}
    is your public key provided by eRepublik and {digest}
    is a hash that represents an encrypted value of a concatenated string
    formed from {resource}, {action}, {params} (if they exist),
    and {date} (the same value Date header has).

    """
    if public_key is None or private_key is None:
        raise Exception("Invalid keys")
    header = {"Auth": public_key + '/'}
    date = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    header["Date"] = date
    to_digest = (url.replace('/', ':').replace('?', ':') + ':').lower() + date
    if version_info >= (3, 0):
        # 3.X behavior is correct. Since HMAC operates on bytes, not text,
        # only bytes are accepted. In Python 2, the acceptance of
        # Unicode strings is more an accident than a feature.
        header["Auth"] += hmac.new(bytes(private_key, 'utf-8'),
                                   bytes(to_digest, 'utf-8'),
                                   sha256).hexdigest()
    else:
        header["Auth"] += hmac.new(private_key,
                                   to_digest,
                                   sha256).hexdigest()
    return header


def _load(url, headers):
    """
    Returns json/dictionary of data in "message" from API response
    """
    req = Request(api_url + url)
    req.add_header("Date", headers["Date"])
    req.add_header("Auth", headers["Auth"])
    response = urlopen(req)
    content = response.read().decode("utf-8")
    data = json.loads(content)
    if data["code"] != 200:
        raise #TODO: Remove custom exceptions and go with standard ones
    else:
        return data["message"]