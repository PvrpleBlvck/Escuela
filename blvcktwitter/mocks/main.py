try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


import requests


from mocks.urls import BASE_URL

MSGS_URL = urljoin(BASE_URL, 'messages')


def get_msgs():
    response = requests.get(MSGS_URL)
    if response.ok:
        return response
    else:
        return None