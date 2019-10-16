# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountDebtCollectionBank(models.Model):
    _name = "account.debt_collection_bank"
    _description = "Debt Collection Bank"
    _inherit = [
        "account.debt_collection_voucher_common",
    ]

    detail_ids = fields.One2many(
        comodel_name="account.debt_collection_bank_detail",
    )
    bank_receipt_id = fields.Many2one(
        string="# Bank Receipt",
        comodel_name="account.bank_receipt",
        ondelete="cascade",
    )
    allowed_journal_ids = fields.Many2many(
        string="Allowed Bank Receipt Journals",
        comodel_name="account.journal",
        related="debt_collection_id.allowed_journal_br_ids",
        store=False,
    )
    payment_mode_id = fields.Many2one(
        string="Payment Mode",
        comodel_name="payment.mode",
    )

    @api.multi
    def _check_bank_receipt_cancel(self):
        self.ensure_one()
        result = True
        obj_bank_receipt =\
            self.env["account.bank_receipt"]
        if self.bank_receipt_id:
            criteria = [
                ("state", "not in", ["draft", "cancel"]),
                ("id", "=", self.bank_receipt_id.id)
            ]
            post_count = obj_bank_receipt.search_count(criteria)
            if post_count > 0:
                result = False
        return result
