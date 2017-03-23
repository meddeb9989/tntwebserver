#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile') #1 to 1 link with Django User
    activation_key = models.CharField(max_length=40)

    def __str__(self):
        try:
            user = User.objects.get(id=self.user.id)
            aff = user.first_name + ' ' + user.last_name
        except Exception:
            aff = str(self.id)
        return aff


class Employe(models.Model):
    user = models.OneToOneField(User, default=1)
    num_carte = models.ForeignKey('Carte', on_delete=models.CASCADE)
    email = models.EmailField()
    id_employeur = models.ForeignKey('Employeur', on_delete=models.CASCADE)

    def __str__(self):
        try:
            user = User.objects.get(id=self.user.id)
            aff = user.first_name + ' ' + user.last_name
        except Exception:
            aff = str(self.id)
        return aff


class Employeur(models.Model):
    user = models.OneToOneField(User, default=1)
    societe = models.TextField(max_length=250)
    email = models.EmailField()

    def __str__(self):
        try:
            user = User.objects.get(id=self.user.id)
            aff = user.first_name + ' ' + user.last_name
        except Exception:
            aff = str(self.id)
        return aff


class Commercant(models.Model):
    user = models.OneToOneField(User, default=1)
    societe = models.TextField(max_length=250)
    email = models.EmailField()

    def __str__(self):
        try:
            user = User.objects.get(id=self.user.id)
            aff = user.first_name + ' ' + user.last_name
        except Exception:
            aff = str(self.id)
        return aff


class Carte(models.Model):
    code = models.IntegerField()
    num_carte = models.BigIntegerField()
    date_expiration = models.DateTimeField()
    valide = models.BooleanField()
    solde = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        try:
            emp = Employe.objects.get(num_carte=self)
            aff = str(self.id)+" : "+emp.user.first_name + ' ' + emp.user.last_name +' : '+ str(self.num_carte)
        except Exception:
            aff = str(self.id)+u" : Non Affectée : "+str(self.num_carte)
        return aff


class Transaction(models.Model):
    id_employe = models.ForeignKey('Employe', on_delete=models.CASCADE)
    id_commercant = models.ForeignKey('Commercant', on_delete=models.CASCADE)
    date = models.DateTimeField()
    confirmed = models.BooleanField(default=False)
    montant = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return "Employe: " + str(self.id_employe) + " Commercant: " + str(self.id_commercant) + " Date: " + str(self.date)


class Recharge(models.Model):
    id_employeur = models.ForeignKey('Employeur', on_delete=models.CASCADE)
    id_employe = models.ForeignKey('Employe', default=False, on_delete=models.CASCADE)
    montant_employe = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return "Employeur : " + str(self.id_employeur) +  " Employe : " + str(self.id_employe) +" Date: " + str(self.date)

class AutoRecharge(models.Model):
    id_employeur = models.ForeignKey('Employeur', on_delete=models.CASCADE)
    id_employe = models.ForeignKey('Employe', default=False, on_delete=models.CASCADE)
    montant_employe = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return "Employeur : " + str(self.id_employeur) +  " Employe : " + str(self.id_employe) +" Date: " + str(self.date)
