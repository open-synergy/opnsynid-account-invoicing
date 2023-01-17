# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Automatic Reverse Deferred Revenue",
    "version": "11.0.1.2.0",
    "license": "LGPL-3",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "account_invoice_reversal",
        "account_deferred_revenue",
    ],
    "data": [
        "wizards/account_asset_reverse_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
