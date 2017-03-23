#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from webserver.serverapp.models import AutoRecharge, Profile, Employe, Employeur, Commercant, Carte, Transaction, Recharge


admin.site.register(Employe)
admin.site.register(Employeur)
admin.site.register(Commercant)
admin.site.register(Transaction)
admin.site.register(Recharge)
admin.site.register(Carte)
admin.site.register(Profile)
admin.site.register(AutoRecharge)
AdminSite.site_title = ugettext_lazy('TAN & TECH ADMIN')
AdminSite.site_header = ugettext_lazy('TAN & TECH ADMINISTRATION')
AdminSite.index_title = ugettext_lazy('DATA BASE ADMINISTRATION')

