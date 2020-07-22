# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Invoicing Multiple Approval Workflow Policy",
    "version": "8.0.1.0.0",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "account_invoice_multiple_approval",
        "account_invoice_workflow_policy",
    ],
    "data": [
        "data/base_workflow_policy_data.xml",
        "views/account_journal_views.xml",
        "views/account_invoice_views.xml",
    ],
}
