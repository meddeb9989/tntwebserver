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
from rest_framework.permissions import AllowAny
from .permissions import IsStaffOrTargetUser
from rest_framework.decorators import api_view


try:
    from collections import OrderedDict
except ImportError:    
    from odict import odict as OrderedDict


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    model = User
 
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),


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
        request.session.set_expiry(30)
        request.session['member_id'] = user.id
        data = [{'valid' : True, 'id' : user.id}]
    else:
        data = [{'valid' : False, 'Error' : u'Login ou mot de passe Incorrect'}]

    return JSONResponse(data)

def logout_view(request):
    logout(request)
    try:
        del request.session['member_id']
    except KeyError:
        pass
    data = [{'valid' : True}]
    return JSONResponse(data)

def please_login(request):
    logout_view(request)
    try:
        del request.session['member_id']
    except KeyError:
        pass
    data = [{'valid' : False, 'Error' : u'Please Login'}]
    return JSONResponse(data)

@api_view(['POST','GET'])
def get_user(request):
    if request.user.is_authenticated():
        usr_type = ""
        group = ""
        user_type=detect_user_type(request.user.id)
        groups=request.user.groups.all()

        if len(groups)>1:
            group = str(groups[0].name) + "&" + str(groups[1].name)
        else:
            group = str(groups[0].name)

        if isinstance(user_type, Employe):
            usr_type = u'Employe'
        elif isinstance(user_type, Employeur):
            usr_type = u'Employeur'
        elif isinstance(user_type, Commercant):
            usr_type = u'Trader'

        data = [{'valid' : True, 'id':request.user.id, 'group': group, 'type': usr_type, 'name' : request.user.first_name+" "+request.user.last_name}]
    else:
        data = [{'valid' : False, 'Error' : u'Please Login'}]

    return JSONResponse(data)

@api_view(['POST','GET'])
def get_amount(request):
    if request.user.is_authenticated():
        user_type=detect_user_type(request.user.id)
        if user_type is not None:
            if isinstance(user_type, Employe):
                carte = user_type.num_carte
                solde = carte.solde
                data = [{'valid' : True, 'amount': solde}]
            else:
                data = [{'valid' : False, 'Error' : u'User not Employe'}]
        else:
            data = [{'valid' : False, 'Error' : u'User not Found'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please Login'}]

    return JSONResponse(data)

@api_view(['POST','GET'])
def bloc_card(request):
    if request.user.is_authenticated():
        user_type=detect_user_type(request.user.id)
        if user_type is not None:
            if isinstance(user_type, Employe):
                carte = user_type.num_carte
                carte.valide = False
                carte.save()
                data = [{'valid' : True}]
            else:
                data = [{'valid' : False, 'Error' : u'User not Employe'}]
        else:
            data = [{'valid' : False, 'Error' : u'User not Found'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please Login'}]

    return JSONResponse(data)

@api_view(['POST','GET'])
def bloc_card_id(request, ids):
    if request.user.is_authenticated():
        user_type=detect_user_type(request.user.id)
        if user_type is not None:
            carte = Carte.objects.get(id=int(ids))
            carte.valide = False
            carte.save()
            data = [{'valid' : True}]
        else:
            data = [{'valid' : False, 'Error' : u'User not Found'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please Login'}]

    return JSONResponse(data)

@api_view(['POST','GET'])
def card_state(request):
    if request.user.is_authenticated():
        user_type=detect_user_type(request.user.id)
        if user_type is not None:
            if isinstance(user_type, Employe):
                carte = user_type.num_carte
                data = [{'valid' : carte.valide}]
            else:
                data = [{'valid' : False, 'Error' : u'User not Employe'}]
        else:
            data = [{'valid' : False, 'Error' : u'User not Found'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please Login'}]

    return JSONResponse(data)

@api_view(['POST','GET'])
def get_card(request, ids):
    if request.user.is_authenticated():
        try:
            data = []
            user_type=detect_user_type(request.user.id)
            if user_type is not None:
                if isinstance(user_type, Employeur) or isinstance(user_type, Employe):
                    try:
                        card = Carte.objects.get(id=int(ids))
                        employe = Employe.objects.get(num_carte=card)
                        crd = {'id':card.id, 'Carte' : str(card.num_carte), 'Date': card.date_expiration, 'valid_card': card.valide, 'Nom': str(employe)}
                        print crd
                        print employe
                        print card
                        data = [{'valid' : True}]
                        data.append(crd)
                    except Exception as e:
                        data = [{'valid' : False, 'Error' : u'Pas de Carte'}]
                else:
                    data = [{'valid' : False, 'Error' : u'Permissions Denied'}]
                
            else:
                data = [{'valid' : False, 'Error' : u'No User Found'}]
        except Exception:
            data = [{'valid' : False, 'Error' : u'Pas de Cartes'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please login'}]

    return JSONResponse(data)

@api_view(['POST','GET'])
def get_cards(request):
    if request.user.is_authenticated():
        try:
            data = []
            user_type=detect_user_type(request.user.id)
            if user_type is not None:
                card = None
                emplyes = None
                if isinstance(user_type, Employeur):
                    try:
                        employes = Employe.objects.filter(id_employeur=user_type)
                        data = [{'valid' : True}]
                        for employe in employes:
                            card = Carte.objects.get(employe=employe)
                            crd = {'id':card.id, 'Carte' : str(card.num_carte), 'Date': card.date_expiration, 'valid_card': card.valide, 'Nom': str(employe)}
                            data.append(crd)
                    except Exception as e:
                        data = [{'valid' : False, 'Error' : u'Pas de Cartes'}]
                else:
                    data = [{'valid' : False, 'Error' : u'Permissions Denied'}]
                
            else:
                data = [{'valid' : False, 'Error' : u'No User Found'}]
        except Exception:
            data = [{'valid' : False, 'Error' : u'Pas de Cartes'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please login'}]

    return JSONResponse(data)

@api_view(['POST','GET'])
def get_rh_cads(request):
    if request.user.is_authenticated():
        try:
            data = []
            user=detect_user_type(request.user.id)
            user_type=user.id_employeur
            if user_type is not None:
                card = None
                emplyes = None
                if isinstance(user_type, Employeur):
                    try:
                        employes = Employe.objects.filter(id_employeur=user_type)
                        data = [{'valid' : True}]
                        for employe in employes:
                            card = Carte.objects.get(employe=employe)
                            crd = {'id':card.id, 'Carte' : str(card.num_carte), 'Date': card.date_expiration, 'valid_card': card.valide, 'Nom': str(employe)}
                            data.append(crd)
                    except Exception as e:
                        print e
                        data = [{'valid' : False, 'Error' : u'Pas de Cartes'}]
                else:
                    data = [{'valid' : False, 'Error' : u'Permissions Denied'}]
                
            else:
                data = [{'valid' : False, 'Error' : u'No User Found'}]
        except Exception:
            data = [{'valid' : False, 'Error' : u'Pas de Cartes'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please login'}]

    return JSONResponse(data)
      

@api_view(['POST','GET'])
def get_all_transactions(request):
    if request.user.is_authenticated():
        try:
            data = []
            user_type=detect_user_type(request.user.id)
            if user_type is not None:
                transactions = None
                if isinstance(user_type, Employe):
                    try:
                        transactions = Transaction.objects.filter(id_employe=user_type)
                        data = [{'valid' : True}]
                        for tran in transactions:
                            tr = {'id':user_type.id, 'Transaction' : str(tran.id_commercant), 'Date': tran.date, 'Montant': str(tran.montant)}
                            data.insert(1, tr)
                    except Exception:
                        data = [{'valid' : False, 'Error' : u'Pas de Transactions'}]
                elif isinstance(user_type, Commercant):
                    try:
                        transactions = Transaction.objects.filter(id_commercant=user_type)
                        data = [{'valid' : True}]
                        for tran in transactions:
                            tr = {'id':user_type.id, 'Transaction' : str(tran.id_employe), 'Date': tran.date, 'Montant': str(tran.montant)}
                            data.insert(1, tr)
                    except Exception:
                        data = [{'valid' : False, 'Error' : u'Pas de Transactions'}]
                
            else:
                data = [{'valid' : False, 'Error' : u'No User Found'}]
        except Exception:
            data = [{'valid' : False, 'Error' : u'Pas de Transactions'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please login'}]

    return JSONResponse(data)

@api_view(['POST','GET'])
def valid_card(request, number):
    if request.user.is_authenticated():
        try:
            carte = Carte.objects.get(num_carte=int(number))
            data = card_validity(carte)
        except Exception:
            data = [{'valid' : False, 'Error' : u'Carte non reconnu'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please login'}]

    return JSONResponse(data)

@api_view(['POST','GET'])
def create_user(request, username, password, first_name, last_name, email):
    try:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, email=email, is_superuser=False, is_active=False, is_staff=False, last_login=date, date_joined=date)
        data = [{'valid' : True}]
    except Exception:
        data = [{'valid' : False, 'Error' : u'Vérifier les champs'}]
    return JSONResponse(data)

@api_view(['POST','GET'])
def recharge_card(request, ids, amount):
    if request.user.is_authenticated():
        try:
            carte = Carte.objects.get(id=int(ids))
            data = amount_add_validity(carte, int(amount))
            if data[0]['valid']:
                employe = Employe.objects.get(num_carte=carte)
                carte.solde=carte.solde+int(amount)
                carte.save()

                myemail = SendEmail()
                myemail.send_email_recharge_valid(str(amount), employe.email, str(employe))

        except Exception as e:
            print e
            data = [{'valid' : False, 'Error' : u'Recharge non effectuée'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please login'}]
    print data
    return JSONResponse(data)

@api_view(['POST','GET'])
def valid_transaction(request, number, code, amount):
    if request.user.is_authenticated():
        try:
            carte = Carte.objects.get(num_carte=number)
            data = amount_validity(carte, code, amount)
            if data[0]['valid']:
                employe = Employe.objects.get(num_carte=carte)
                commercant = Commercant.objects.get(user=int(request.user))
                date = datetime.now()

                Transaction.objects.create(id_employe=employe, id_commercant=commercant, date=date, montant=int(amount))
                carte.solde=carte.solde-int(amount)
                carte.save()

                myemail = SendEmail()
                myemail.send_email_transaction_valid(str(amount), str(commercant), employe.email, commercant.email, str(employe))

        except Exception:
            data = [{'valid' : False, 'Error' : u'Transaction non effectuée'}]
    else:
        data = [{'valid' : False, 'Error' : u'Please login'}]

    return JSONResponse(data)

def card_validity(carte):
    if carte.valide:
        date = datetime.now()
        print carte.date_expiration, date
        if carte.date_expiration > date:
            data = [{'valid' : True}]
        else:
            data = [{'valid' : False, 'Error' : u'Carte Expirée'}]
    else:
        data = [{'valid' : False, 'Error' : u'Carte non valide'}]
    print data
    return data

def amount_validity(carte, code, amount):
    data = card_validity(carte)
    if data[0]['valid']:
        if carte.code == int(code):
            if carte.solde > int(amount):
                data = [{'valid' : True}]
            else:
                data = [{'valid' : False, 'Error' : u'Solde Insuffisant'}]
        else:
            data = [{'valid' : False, 'Error' : u'Code Incorrect'}]

    return data

def amount_add_validity(carte, amount):
    if int(amount) > 0 and int(amount) < 9999:
        if carte.solde + int(amount) < 10000:
            data = [{'valid' : True}]
        else:
            data = [{'valid' : False, 'Error' : u'Valeur très grande, Nouveau solde dépasse 9999€ '}]
    else:
        data = [{'valid' : False, 'Error' : u'Valeur Incorrect doit etre comprise entre 0 et 9999'}]

    return data

@method_decorator(csrf_exempt)
def send_email(request):
    myemail = SendEmail()
    myemail.send_email_transaction_valid("19.90", "Farmer's Burger", "meddeb9989@hotmail.fr", "fakher9989@hotmail.fr")
    data = [{'valid' : True}]
    return JSONResponse(data)

def detect_user_type(user_id):
    #user_id=request.session['member_id']
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
                data = [{'valid' : False, 'Error' : u'No User Found'}]
    print user_type
    return user_type
