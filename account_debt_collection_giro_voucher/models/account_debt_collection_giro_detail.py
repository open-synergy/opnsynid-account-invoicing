# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountDebtCollectionGiroDetail(models.Model):
    _name = "account.debt_collection_giro_detail"
    _description = "Debt Collection Giro Detail"
    _inherit = [
        "account.debt_collection_voucher_detail_common",
    ]

    collection_voucher_id = fields.Many2one(
        comodel_name="account.debt_collection_giro",
    )
    giro_receipt_line_id = fields.Many2one(
        string="# Giro Receipt Line",
        comodel_name="account.giro_receipt_line",
    )
