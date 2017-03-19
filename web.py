import json
import requests
import sys


session = requests.Session()

def post_data_to_url(url, header=None, data=None):
    req = session.post(url, headers=header, data=data)
    return req.status_code, req.text


def get_json_data_from_post(url, header, data):
    status, text = post_data_to_url(url, header, data)
    return json.loads(text)
