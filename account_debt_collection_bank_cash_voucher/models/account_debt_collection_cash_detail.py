# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountDebtCollectionCashDetail(models.Model):
    _name = "account.debt_collection_cash_detail"
    _description = "Debt Collection Cash Detail"
    _inherit = [
        "account.debt_collection_voucher_detail_common",
    ]

    collection_voucher_id = fields.Many2one(
        comodel_name="account.debt_collection_cash",
    )
    cash_receipt_line_id = fields.Many2one(
        string="# Cash Receipt",
        comodel_name="account.cash_receipt_line",
        ondelete="restrict",
    )
