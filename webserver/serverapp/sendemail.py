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
    """docstring for Email"""
    def __init__(self, **kwargs):
        super(SendEmail, self).__init__(**kwargs)
        

    def send_email_validation_user(self, name, key, email):
        try:
            import smtplib 
            src = 'tanndtech@gmail.com'
            password = 'msif2017'
            dest = email
            my_email = GetEmail()
            my_email.set_valid_email(name, key)
            print email
            message = my_email.get_valid_email()

            mail = message
            smtp = smtplib.SMTP('smtp.gmail.com') 
            smtp.set_debuglevel(1) 
            smtp.ehlo() 
            smtp.starttls() 
            smtp.ehlo() 
            smtp.login(src, password) 
            smtp.sendmail(src, dest, mail) 
            smtp.close() 

            #gmail_user = 'tanndtech@gmail.com'
            #password = 'msif2017'
            #yag = yagmail.SMTP(user=gmail_user, password=password)
            #my_email = GetEmail()
            #my_email.set_valid_email(name, key)
            #print email
            #message = my_email.get_valid_email()
            #if email == "meddeb9989@hotmail.fr":
            #    print email
            #Subject = 'Activation compte AVENTIX'
            #yag.send(email, subject=Subject, contents=message, headers={"From":"TAN & TECH", "To":email})
        except Exception as e:
            print e
  
    def send_email_transaction_valid(self, amount, trader, email_employee, email_trader, employe):
        gmail_user = 'tanndtech@gmail.com'
        password = 'msif2017'
        yag = yagmail.SMTP(user=gmail_user, password=password)
        png_file_names = "webserver/serverapp/tanandtech.png"
        email_employee=str(unicode(email_employee))
        email_trader=str(unicode(email_trader))
        my_email = GetEmail()
        my_email.set_transaction_email(amount, trader, employe)

        message_employee = my_email.get_transaction_email()
        Subject_employee = 'Reçu pour votre paiement à ' + trader 
        yag.send(email_employee, subject=Subject_employee, contents=message_employee, headers={"From":"TAN & TECH", "To":email_employee})

        message_trader = my_email.get_transaction_email()
        Subject_trader = 'Paiement Reçu '
        yag.send(email_trader, subject=Subject_trader, contents=message_trader, headers={"From":"TAN & TECH", "To":email_trader})
      
    def send_email_recharge_valid(self, amount, email, employe):
        pass

if __name__ == '__main__':
    email = SendEmail()
    email.send_email_validation_user("INSA LYON", "bdu3od348td874yx393", "meddeb9989@hotmail.fr")
