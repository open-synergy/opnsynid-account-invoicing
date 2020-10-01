# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Invoice Workflow Policy",
    "version": "8.0.1.2.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
        "base_workflow_policy",
    ],
    "data": [
        "data/base_workflow_policy_data.xml",
        "views/account_journal_views.xml",
        "views/account_invoice_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
