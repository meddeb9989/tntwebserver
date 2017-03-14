#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'meedbmohamedfakher'
import sys  
import os
import yagmail
from webserver.serverapp.getemail import my_email

reload(sys)  
sys.setdefaultencoding('utf8')


class SendEmail(object):
      """docstring for Email"""
      def __init__(self, **kwargs):
            super(SendEmail, self).__init__(**kwargs)
  
      def send_email_transaction_valid(self, amount, trader, email_employee, email_trader):
  
            gmail_user = 'tanndtech@gmail.com'
            password = 'msif2017'
            yag = yagmail.SMTP(user=gmail_user, password=password)
            png_file_names = "webserver/serverapp/tanandtech.png"
            email_employee=str(unicode(email_employee))
            email_trader=str(unicode(email_trader))
            print amount, trader, email_employee, email_trader, png_file_names
    
            #message_employee = "Bonjour Monsieur,\n \n" \
            #+ "Votre paiement de €" + amount + " EUR à " + trader + ", a été effectué avec succès. \n \n"\
            #+ "Il est possible que la transaction n'apparaisse qu'au bout de quelques minutes sur votre compte. \n\n" \
            #+ "Marchand \n"\
            #+ trader + "\n"\
            #+ email_trader
            message_employee = my_email
            Subject_employee = 'Reçu pour votre paiement à ' + trader 
            yag.send(email_employee, subject=Subject_employee, contents=message_employee, headers={"From":"TAN & TECH", "To":email_employee})
            print "Email Envoyée"
           # message_trader = "Bonjour " +trader +",\n \n" \
           # + "Paiement Reçu  avec succès d'un montant de €" + amount + " EUR. \n \n"\
           # + "Il est possible que la transaction n'apparaisse qu'au bout de quelques minutes sur votre compte. \n\n" \
           # + "AVENTIX \n"\
           # + "TAN & TECH\n"\
           # + gmail_user
            message_trader = my_email
            Subject_trader = 'Paiement Reçu '
            yag.send(email_trader, subject=Subject_trader, contents=message_trader, headers={"From":"TAN & TECH", "To":email_trader})

if __name__ == '__main__':
    email = SendEmail()
    email.send_email_transaction_valid("19", "INSA LYON", "meddeb9989@hotmail.fr", "mohamed-fakher.meddeb@insa-lyon.fr")
