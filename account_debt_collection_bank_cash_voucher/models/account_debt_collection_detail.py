# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class AccountDebtCollectionDetail(models.Model):
    _inherit = "account.debt_collection_detail"

    @api.multi
    def get_amount_collected_all(self):
        _super = super(AccountDebtCollectionDetail, self)
        result = _super.get_amount_collected_all()
        amount_bank_collected =\
            self.amount_bank_collected
        amount_cash_collected =\
            self.amount_cash_collected
        amount_bank_cash =\
            (amount_bank_collected + amount_cash_collected)
        result += amount_bank_cash
        return result

    @api.multi
    @api.depends(
        "amount_bank_collected",
        "amount_cash_collected",
    )
    def _compute_amount_collected(self):
        _super = super(AccountDebtCollectionDetail, self)
        _super._compute_amount_collected()

    @api.multi
    @api.depends(
        "debt_collection_id.bank_detail_ids",
        "debt_collection_id.bank_detail_ids.detail_ids",
        "debt_collection_id.bank_detail_ids.detail_ids.amount",
    )
    def _compute_bank_collected_amount(self):
        for document in self:
            amount_bank_collected = 0.0
            bank_detail_ids =\
                document.debt_collection_id.bank_detail_ids
            if bank_detail_ids:
                for bank_detail in bank_detail_ids:
                    detail_ids = bank_detail.detail_ids
                    for detail in detail_ids.filtered(
                        lambda r: r.collection_detail_id.id == document.id
                    ):
                        amount_bank_collected += detail.amount
                        document.update({
                            "amount_bank_collected": amount_bank_collected,
                        })

    @api.multi
    @api.depends(
        "debt_collection_id.cash_detail_ids",
        "debt_collection_id.cash_detail_ids.amount",
    )
    def _compute_cash_collected_amount(self):
        for document in self:
            amount_cash_collected = 0.0
            cash_detail_ids =\
                document.debt_collection_id.cash_detail_ids
            if cash_detail_ids:
                for cash_detail in cash_detail_ids:
                    detail_ids = cash_detail.detail_ids
                    for detail in detail_ids.filtered(
                        lambda r: r.collection_detail_id.id == document.id
                    ):
                        amount_cash_collected += detail.amount
                        document.update({
                            "amount_cash_collected": amount_cash_collected,
                        })

    amount_bank_collected = fields.Float(
        string="Collected Bank Amount",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_compute_bank_collected_amount",
    )
    amount_cash_collected = fields.Float(
        string="Collected Cash Amount",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_compute_cash_collected_amount",
    )
