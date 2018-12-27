# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Invoice Workflow Policy",
    "version": "8.0.1.0.1",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "views/account_journal_views.xml",
        "views/account_invoice_views.xml",
    ],
}
