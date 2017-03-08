#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
import django
from django.conf import settings
from webserver.serverapp.models import Carte
from datetime import date
from django.test.utils import setup_test_environment
setup_test_environment()


class CardTests(TestCase):
    """docstring for Tests"""

    def create_card(self):
    	"""Create Card"""
        dates=date(2017, 9, 4)
        solde=900.00
        valide=True
        num=input("donner numero carte\n")
        code=3344
        Carte.objects.create(code=code, num_carte=num, valide=valide, solde=solde, date_expiration=dates)
        print "Card "+str(num)+" created successfully"

    def find_card(self):
        """Find Our Card"""
        num=input("donner numero carte\n")
        try:
            lion = Carte.objects.get(num_carte=num)
        except Carte.DoesNotExist:
            print str(num)+ " Does Not Exist\n"
            lion = Carte.objects.all()
        
        print lion
        
