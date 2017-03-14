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
from sendemail import SendEmail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
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

def login_view(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        request.session.set_expiry(700)
        request.session['member_id'] = user.id
        data = [{'valide' : u'Login success'}]
    else:
        data = [{'valide' : u'Login ou mot de passe Incorrect'}]

    return JSONResponse(data)

def logout_view(request):
    logout(request)
    try:
        del request.session['member_id']
    except KeyError:
        pass
    data = [{'valide' : u'Logout success'}]
    return JSONResponse(data)

def please_login(request):
    logout_view(request)
    try:
        del request.session['member_id']
    except KeyError:
        pass
    data = [{'valide' : u'Please Login'}]
    return JSONResponse(data)

@method_decorator(csrf_exempt)
def get_all_transactions(request):
    try:
        data = []
        user_type=detect_user_type(request)
        print user_type
        if user_type is not None:
            transactions = None
            try:
                transactions = Transaction.objects.filter(id_employe=user_type)
            except Exception:
                try:
                    transactions = Transaction.objects.filter(id_commercant=user_type)
                except Transaction.DoesNotExist:
                    data = [{'valide' : u'Pas de Transactions'}]
            
            data = [{'valide' : u'Transactions'}]
            for tran in transactions:
                tr = {'id':user_type.id, 'Employe' : str(tran.id_employe), 'Commercant': str(tran.id_commercant), 'Date': str(tran.date), 'Montant': str(tran.montant)}
                data.append(tr)
        else:
            data = [{'valide' : u'No User Found'}]
    except Exception:
        data = [{'valide' : u'Pas de Transactions'}]
    return JSONResponse(data)

@method_decorator(csrf_exempt)
def valid_card(request, number):
    if request.method == 'GET':
        try:
            carte = Carte.objects.get(num_carte=int(number))
            print carte
            data = card_validity(carte)
        except Exception:
            data = [{'valide' : u'Carte non reconnu'}]
        return JSONResponse(data)

@method_decorator(csrf_exempt)
def create_user(request, username, password, first_name, last_name, email):
    try:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, email=email, is_superuser=False, is_active=False, is_staff=False, last_login=date, date_joined=date)
        data = [{'valide' : u'User Créer avec Succès'}]
    except Exception:
        data = [{'valide' : u'Vérifier les champs'}]
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

                myemail = SendEmail()
                myemail.send_email_transaction_valid(str(amount), commercant.societe, employe.email, commercant.email)

        except Exception:
            data = [{'valide' : u'Transaction non effectuée'}]
        return JSONResponse(data)

    elif request.method == 'POST':
        print "on est dans le post : " + number
        return JSONResponse(data)

def card_validity(carte):
    if carte.valide:
        date = datetime.now().date()
        print carte.date_expiration, date
        if carte.date_expiration > date:
            data = [{'valide' : u'valide'}]
        else:
            data = [{'valide' : u'Carte Expirée'}]
    else:
        data = [{'valide', u'Carte non valide'}]
    print data
    return data

def amount_validity(carte, code, amount):
    data = card_validity(carte)
    if data[0]['valide']==u'valide':
        if carte.code == int(code):
            if carte.solde > int(amount):
                data = [{'valide': u'Transaction Validée'}]
            else:
                data = [{'valide' : u'Solde Insuffisant'}]
        else:
            data = [{'valide' : u'Code Incorrect'}]

    return data

@method_decorator(csrf_exempt)
def send_email(request):
    myemail = SendEmail()
    myemail.send_email_transaction_valid("19.90", "Farmer's Burger", "meddeb9989@hotmail.fr", "fakher9989@hotmail.fr")
    data = [{'valide' : u'Email Envoyée'}]
    return JSONResponse(data)

def detect_user_type(request):
    user_id=request.session['member_id']
    user=User.objects.get(id=user_id)
    user_type = None
    try:
        user_type = Employe.objects.get(user=user)
    except Exception:
        try:
            user_type = Employeur.objects.get(user=user)
        except Exception:
            try:
                user_type = Commercant.objects.get(user=user)
            except Exception:
                data = [{'valide' : u'No User Found'}]
    print user_type
    return user_type
