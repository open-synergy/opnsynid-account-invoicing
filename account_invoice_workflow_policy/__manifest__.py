# Copyright 2021 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Account Invoice Workflow Policy",
    "version": "11.0.1.1.0",
    "license": "LGPL-3",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "account_invoice_multiple_approval",
        "ssi_policy_mixin",
    ],
    "data": [
        "data/policy_template_data.xml",
        "views/account_invoice_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
