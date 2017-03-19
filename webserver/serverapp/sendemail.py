#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'meedbmohamedfakher'
import sys  
import os
import yagmail
from webserver.serverapp.getemail import GetEmail

reload(sys)  
sys.setdefaultencoding('utf8')


class SendEmail(object):
      yag = None

      """docstring for Email"""
      def __init__(self, **kwargs):
            super(SendEmail, self).__init__(**kwargs)
            gmail_user = 'tanndtech@gmail.com'
            password = 'msif2017'
            self.yag = yagmail.SMTP(user=gmail_user, password=password)
  
      def send_email_transaction_valid(self, amount, trader, email_employee, email_trader, employe):
            png_file_names = "webserver/serverapp/tanandtech.png"
            email_employee=str(unicode(email_employee))
            email_trader=str(unicode(email_trader))
            my_email = GetEmail()
            my_email.set_transaction_email(amount, trader, employe)

            message_employee = my_email.get_transaction_email()
            Subject_employee = 'Reçu pour votre paiement à ' + trader 
            self.yag.send(email_employee, subject=Subject_employee, contents=message_employee, headers={"From":"TAN & TECH", "To":email_employee})

            message_trader = my_email.get_transaction_email()
            Subject_trader = 'Paiement Reçu '
            self.yag.send(email_trader, subject=Subject_trader, contents=message_trader, headers={"From":"TAN & TECH", "To":email_trader})
      
      def send_email_recharge_valid(self, amount, email, employe):
        pass

if __name__ == '__main__':
    email = SendEmail()
    email.send_email_transaction_valid("19", "INSA LYON", "meddeb9989@hotmail.fr", "mohamed-fakher.meddeb@insa-lyon.fr")
