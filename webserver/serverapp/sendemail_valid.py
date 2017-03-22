#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'meedbmohamedfakher'
import sys  
import os
import yagmail
from webserver.serverapp.getemail import GetEmail

reload(sys)  
sys.setdefaultencoding('utf8')


class SendEmailValid(object):
    """docstring for Email"""
    def __init__(self, **kwargs):
        super(SendEmailValid, self).__init__(**kwargs)
        

    def send_email_validation_user(self, name, key, email):
        try:
            gmail_user = 'tanndtech@gmail.com'
            password = 'msif2017'
            yag = yagmail.SMTP(user=gmail_user, password=password)
            my_email = GetEmail()
            my_email.set_valid_email(name, key)
            print email
            message = my_email.get_valid_email()
            if email == "meddeb9989@hotmail.fr":
                print email
            Subject = 'Activation compte AVENTIX'
            yag.send(email, subject=Subject, contents=message, headers={"From":"TAN & TECH", "To":email})
        except Exception as e:
            print e