#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from webserver.serverapp.serializers import UserSerializer, GroupSerializer
from webserver.serverapp.models import Carte, Transaction, Commercant, Employe, Employeur, Recharge

from datetime import datetime

try:
    from collections import OrderedDict
except ImportError:    
    from odict import odict as OrderedDict


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class JSONResponse(HttpResponse):
    """docstring for JSONResponse"""
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


        
@method_decorator(csrf_exempt)
def valid_card(request, number):
    if request.method == 'GET':
        try:
            carte = Carte.objects.get(num_carte=number)
            data = card_validity(carte)
        except Carte.DoesNotExist:
            data = [{'valide' : u'Carte non reconnu'}]
        return JSONResponse(data)

@method_decorator(csrf_exempt)
def valid_transaction(request, number, code, amount, trader):
    if request.method == 'GET':
        try:
            carte = Carte.objects.get(num_carte=number)
            data = amount_validity(carte, code, amount)
            if data[0]['valide']==u'Transaction Validée':
                employe = Employe.objects.get(num_carte=carte)
                commercant = Commercant.objects.get(id=int(trader))
                date = datetime.now().date()

                Transaction.objects.create(id_employe=employe, id_commercant=commercant, date=date, montant=int(amount))
                carte.solde=carte.solde-int(amount)
                carte.save()
        except Carte.DoesNotExist or Employe.DoesNotExist or Commercant.DoesNotExist:
            data = [{'valide' : u'Transaction non effectuée'}]
        return JSONResponse(data)

    elif request.method == 'POST':
        print "on est dans le post : " + number
        return JSONResponse(data)

def card_validity(carte):
    if carte.valide:
        if carte.date_expiration > datetime.now().date():
            data = [{'valide' : u'valide'}]
        else:
            data = [{'valide' : u'Carte Expirée'}]
    else:
        data = [{'valide', u'Carte non valide'}]

    return data

def amount_validity(carte, code, amount):
    data = card_validity(carte)
    print carte.code, code
    if data[0]['valide']==u'valide':
        if carte.code == int(code):
            if carte.solde > int(amount):
                data = [{'valide': u'Transaction Validée'}]
            else:
                data = [{'valide' : u'Solde Insuffisant'}]
        else:
            data = [{'valide' : u'Code Incorrect'}]

    return data
            
