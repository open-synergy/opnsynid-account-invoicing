# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Debt Collection Schedule",
    "version": "8.0.1.0.0",
    "category": "Invocing",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_debt_collection",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_debt_collection_schedule_views.xml",
        "views/account_debt_collection_views.xml",
    ],
}
