# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Invoice Workflow Policy - Account Cancel",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_cancel",
        "account_invoice_workflow_policy",
    ],
    "data": [
        "views/account_invoice_views.xml"
    ],
    "auto_install": True,
}
