# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import gettext

import gtk
import common
from common import openerp_gtk_builder
import service
import rpc

def field_pref_set(field, name, model, value, pwdfield, dependance=None, window=None):
    ui = openerp_gtk_builder('openerp.ui', ['win_field_pref'])
    if dependance is None:
        dependance = []
    if window is None:
        window = service.LocalService('gui.main').window
    win = ui.get_object('win_field_pref')
    win.set_transient_for(window)
    win.set_icon(common.OPENERP_ICON)
    ent = ui.get_object('ent_field')
    ent.set_text(name)
    ent = ui.get_object('ent_domain')
    ent.set_text(model)
    ent = ui.get_object('ent_value')
    ent.set_text((value and str(value)) or '/')
    ent.set_visibility(not pwdfield)
    radio = ui.get_object('radio_user_pref')
    vbox = ui.get_object('pref_vbox')
    widgets = {}
    addwidget = False
    for (fname,fvalue,rname,rvalue) in dependance:
        if rvalue:
            addwidget = True
            widget = gtk.CheckButton(fname+' = '+str(rname))
            widgets[(fvalue,rvalue)] = widget
            vbox.pack_start(widget)
    if not len(dependance) or not addwidget:
        vbox.pack_start(gtk.Label(_('Always applicable !')))
    vbox.show_all()

    res = win.run()

    deps = False
    for nv in widgets.keys():
        if widgets[nv].get_active():
            deps = nv[0]+'='+str(nv[1])
            break
    window.present()
    win.destroy()
    if res==gtk.RESPONSE_OK:
        rpc.session.rpc_exec_auth('/object', 'execute', 'ir.values', 'set', 'default', deps, field, [(model,False)], value, True, False, False, radio.get_active(), True)
        return True
    return False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
