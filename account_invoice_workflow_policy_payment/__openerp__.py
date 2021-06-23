# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Invoice Workflow Policy - " "account_voucher Integration",
    "version": "8.0.1.2.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "account_voucher",
        "account_invoice_workflow_policy",
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
