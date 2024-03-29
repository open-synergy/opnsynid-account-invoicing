# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Debt Collection Bank and Cash",
    "version": "8.0.1.7.1",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "depends": [
        "account_debt_collection_voucher_common",
        "account_voucher_bank_cash",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_debt_collection_type_views.xml",
        "views/account_debt_collection_views.xml",
        "views/account_debt_collection_summary_by_date_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
