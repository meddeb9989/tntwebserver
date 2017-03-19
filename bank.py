#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

website_url="http://127.0.0.1:8000/"
url=website_url+"send_email/"
r=requests.get(url)
print r.text