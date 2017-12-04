#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

login = 'admin'
password = 'msif2017'
website_url = "https://tntbankserver.herokuapp.com/"
r = requests.post(website_url+"api-token-auth/", data={"username": login,"password":password})
token =json.loads(r.text)
data = [{"valid": "Pas de transactions non valides"}]
if u'non_field_errors' in token:
    data = [{'valid' : False}]
else:
    token = token[u'token']
    url=website_url+"transactions/"
    r=requests.get(url, headers={'Authorization': 'Token '+token})
