# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Proforma Invoice",
    "version": "11.0.1.0.0",
    "license": "LGPL-3",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "account",
    ],
    "data": [
        "views/account_journal_views.xml",
        "views/account_invoice_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}