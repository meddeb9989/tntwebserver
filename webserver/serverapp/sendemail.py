#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'meedbmohamedfakher'

import yagmail

class SendEmail(object):
    """docstring for Email"""
    def __init__(self, **kwargs):
        super(SendEmail, self).__init__(**kwargs)

    def send_email_transaction_valid(self, amount, trader, email_employee, email_trader):

        gmail_user = 'tanndtech@gmail.com'
        password = 'msif2017'
        yag = yagmail.SMTP(user=gmail_user, password=password)

        message_employee = "Bonjour Monsieur,\n \n" \
        + "Votre paiement de €" + amount + " EUR à " + trader + ", a été effectué avec succès. \n \n"\
        + "Il est possible que la transaction n'apparaisse qu'au bout de quelques minutes sur votre compte. \n\n" \
        + "Marchand \n"\
        + trader + "\n"\
        + email_trader
        
        Subject_employee = 'Reçu pour votre paiement à ' + trader 

        message_trader = "Bonjour " +trader +",\n \n" \
        + "Paiement Reçu  avec succès d'un montant de €" + amount + " EUR. \n \n"\
        + "Il est possible que la transaction n'apparaisse qu'au bout de quelques minutes sur votre compte. \n\n" \
        + "AVENTIX \n"\
        + "TAN & TECH\n"\
        + gmail_user
        
        Subject_trader = 'Paiement Reçu '

        yag.send(email_employee, subject=Subject_employee, contents=message_employee, headers={"From":"TAN & TECH", "To":email_employee})
        yag.send(email_trader, subject=Subject_trader, contents=message_trader, headers={"From":"TAN & TECH", "To":email_trader})

if __name__ == '__main__':
    email = SendEmail()
    email.send_email_transaction_valid("19", "INSA LYON", "meddeb9989@hotmail.fr", "mohamed-fakher.meddeb@insa-lyon.fr")
