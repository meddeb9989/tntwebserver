#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from serversrc.serverapp.serializers import UserSerializer, GroupSerializer
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

data = [OrderedDict([('id', 1), ('title', u''), ('code', u'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', u''), ('code', u'print "hello, world"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', u''), ('code', u'print "hello, world"'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
        
@method_decorator(csrf_exempt)
def valid_card(request, number):
    if request.method == 'GET':
        print "on est dans le get : " + number
        return JSONResponse(data)
    elif request.method == 'POST':
        print "on est dans le post : " + number
        return JSONResponse(data)