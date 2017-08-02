# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Invoice Line Summary By Product",
    "version": "8.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": False,
    "depends": [
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_invoice_views.xml",
    ],
}
