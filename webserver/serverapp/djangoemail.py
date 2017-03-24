#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from webserver.serverapp.getemail import GetEmail


class DjangoEmail(object):
    """docstring for DjangoEmail"""
    def __init__(self, **kwargs):
        super(DjangoEmail, self).__init__(**kwargs)
        

    def email_one(self):
        subject = "I am a text email"
        to = ['meddeb9989@hotmail.fr']
        from_email = 'tanndtech@gmail.com'
    
        ctx = {
            'user': 'buddy',
            'purchase': 'Books'
        }
    
        message = "render_to_string('Hello', ctx)"
    
        EmailMessage(subject, message, to=to, from_email=from_email).send()
    
        return HttpResponse('email_one')
    
    def email_two(self):
        getemail = GetEmail()
        subject = "Valider votre email"
        to = ['meddeb9989@hotmail.fr']
        from_email = 'tanndtech@gmail.com'
        getemail.set_valid_email("Meddeb", "1223123121331212")
        ctx = {
            'user': 'buddy',
            'purchase': 'Books'
        }
    
        message = getemail.get_valid_email()
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
    
        return HttpResponse('email_two')

    def send_email_validation_user(self, first_name, activation_key, email):
        getemail = GetEmail()
        subject = "Valider votre compte AVENTIX"
        to = [email]
        from_email = 'tanndtech@gmail.com'
        getemail.set_valid_email(str(first_name), str(activation_key))

        message = getemail.get_valid_email()
        msg = EmailMessage(subject, message, to=to, from_email=from_email, headers={"From":"TAN & TECH", "To":email})
        msg.content_subtype = 'html'
        msg.send()
        print "email sent"

        return HttpResponse('email_two')

    def send_email_validation_emp(self, first_name, user_name, password, email, code):
        getemail = GetEmail()
        subject = "Bienvenue à AVENTIX"
        to = [email]
        from_email = 'tanndtech@gmail.com'
        getemail.set_validemp_email(str(first_name), str(user_name), str(password), str(code))

        message = getemail.get_validemp_email()
        msg = EmailMessage(subject, message, to=to, from_email=from_email, headers={"From":"TAN & TECH", "To":email})
        msg.content_subtype = 'html'
        msg.send()
        print "email sent"

        return HttpResponse('email_two')

    def send_email_validation_transaction_employe(self, amount, trader, email_employee, employe):
        getemail = GetEmail()
        subject = 'Reçu pour votre paiement à ' + trader 
        email=str(unicode(email_employee))
        to = [email]
        from_email = 'tanndtech@gmail.com'
        getemail.set_transaction_email(amount, trader, employe)

        message = getemail.get_transaction_email()
        msg = EmailMessage(subject, message, to=to, from_email=from_email, headers={"From":"TAN & TECH", "To":email})
        msg.content_subtype = 'html'
        msg.send()
        print "email sent"

        return HttpResponse('email_two')

    def send_email_validation_transaction_trader(self, amount, trader, email_trader):
        getemail = GetEmail()
        subject = 'Paiement Reçu ' 
        email=str(unicode(email_trader))
        to = [email]
        from_email = 'tanndtech@gmail.com'
        getemail.set_trader_email(trader, amount)

        message = getemail.get_trader_email()
        msg = EmailMessage(subject, message, to=to, from_email=from_email, headers={"From":"TAN & TECH", "To":email})
        msg.content_subtype = 'html'
        msg.send()
        print "email sent"

        return HttpResponse('email_two')

    def send_email_validation_recharge(self, amount, email_employee, employe, montant_employe, solde):
        getemail = GetEmail()
        subject = 'Recharge effectuée par votre employeur' 
        email=str(unicode(email_employee))
        to = [email]
        from_email = 'tanndtech@gmail.com'
        getemail.set_email_validation_recharge(amount, employe, montant_employe, solde)

        message = getemail.get_email_validation_recharge()
        msg = EmailMessage(subject, message, to=to, from_email=from_email, headers={"From":"TAN & TECH", "To":email})
        msg.content_subtype = 'html'
        msg.send()
        print "email sent"

        return HttpResponse('email_two')


if __name__ == '__main__':
    email_one()
    email_two()