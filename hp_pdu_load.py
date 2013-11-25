#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    check_hp_pdu: a script to check HP PDU Management Module
#    Copyright (C) 2013  Lorenzo Dalrio <lorenzo.dalrio@cup2000.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Lorenzo Dalrio <lorenzo.dalrio@cup2000.it>"
__copyright__ = "Copyright (C) 2013  Lorenzo Dalrio <lorenzo.dalrio@cup2000.it>"
__license__ = "GPL 3.0"


# set default value of variable (user can override in main.mk)
hp_pdu_load_default_values = (80, 90)


def inventory_hp_pdu_load(info):
    inventory = []
    for pdu, load in info:
        inventory.append((pdu, "hp_pdu_load_default_values"))
    return inventory


def check_hp_pdu_load(item, params, info):
    warn, crit = params
    for line in info:
        if line[0] == item:
            load = int(line[1])
            perfdata = [("load", load, warn, crit)]
            if load > crit:
                return 2, "PDU Load is %d%%" % load, perfdata
            elif load > warn:
                return 1, "PDU Load is %d%%" % load, perfdata
            else:
                return 0, "PDU Load is %d%%" % load, perfdata
    return 3, "PDU %d not found" % item


check_info["hp_pdu_load"] = {
    'check_function': check_hp_pdu_load,
    'inventory_function': inventory_hp_pdu_load,
    'service_description': "PDU %s Load",
    'has_perfdata': True,
}

# BASE: .1.3.6.1.4.1.232.165
snmp_info["hp_pdu_load"] = (".1.3.6.1.4.1.232.165",
                            [
                                "2.3.1.1.1",  # CPQPOWER-MIB::pduOutputIndex
                                "2.3.1.1.2",  # CPQPOWER-MIB::pduOutputLoad
                            ]
                            )

snmp_scan_functions["hp_pdu_load"] = lambda oid: oid(".1.3.6.1.2.1.1.1.0").lower().startswith('hp pdu')