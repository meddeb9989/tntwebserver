#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from webserver.serverapp.models import Employe, Employeur, Commercant, Carte, Transaction, Recharge


admin.site.register(Employe)
admin.site.register(Employeur)
admin.site.register(Commercant)
admin.site.register(Transaction)
admin.site.register(Recharge)
admin.site.register(Carte)
