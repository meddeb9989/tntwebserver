#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


password_pattern = r'[A-Za-z0-9@#$%^&+=]'
username_pattern = r'[a-zA-Z0-9_.-]'
first_name_pattern = r'[a-zA-Z ]'
last_name_pattern = r'[a-zA-Z ]'
email_pattern = r'[a-zA-Z0-9_.@-]'
number_pattern = r'[0-9]'

if re.match(pattern, wod):
    # match
else:
    # no match