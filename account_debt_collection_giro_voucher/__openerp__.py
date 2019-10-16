# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Debt Collection Giro",
    "version": "8.0.1.1.0",
    "category": "Invoicing",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "depends": [
        "account_debt_collection_voucher_common",
        "account_voucher_giro",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_debt_collection_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
