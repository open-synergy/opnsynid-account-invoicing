# Copyright 2021 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Workflow Policy",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "account_invoice_multiple_approval",
        "ssi_policy_mixin",
    ],
    "data": [
        "views/account_invoice_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
