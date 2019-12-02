# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Debt Collection",
    "version": "8.0.1.5.0",
    "category": "Invoicing",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_print_policy",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "menu.xml",
        "wizards/wizard_import_invoice.xml",
        "views/account_debt_collection_type_views.xml",
        "views/account_debt_collection_views.xml",
        "views/res_partner_views.xml",
        "views/account_debt_collection_summary_by_date_views.xml",
        "views/account_invoice_views.xml",
    ],
}
