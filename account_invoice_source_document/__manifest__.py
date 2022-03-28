# Copyright 2021 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Account Invoice Source Document",
    "version": "11.0.1.1.0",
    "license": "LGPL-3",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "account",
        "ssi_source_document_mixin",
    ],
    "data": [
        "views/account_invoice_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
