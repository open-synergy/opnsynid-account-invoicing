# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Debt Collection Voucher Common",
    "version": "8.0.1.2.0",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "depends": [
        "account_debt_collection",
        "account_voucher_common",
    ],
    "data": [
        "views/account_debt_collection_type_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
