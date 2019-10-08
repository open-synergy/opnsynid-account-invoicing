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
        amount_cheque_collected =\
            self.amount_cheque_collected
        result += amount_cheque_collected
        return result

    @api.multi
    @api.depends(
        "amount_cheque_collected",
    )
    def _compute_amount_collected(self):
        _super = super(AccountDebtCollectionDetail, self)
        _super._compute_amount_collected()

    @api.multi
    @api.depends(
        "debt_collection_id.cheque_detail_ids",
        "debt_collection_id.cheque_detail_ids.detail_ids",
        "debt_collection_id.cheque_detail_ids.detail_ids.amount",
    )
    def _compute_cheque_collected_amount(self):
        for document in self:
            amount_cheque_collected = 0.0
            cheque_detail_ids =\
                document.debt_collection_id.cheque_detail_ids
            if cheque_detail_ids:
                for cheque_detail in cheque_detail_ids:
                    detail_ids = cheque_detail.detail_ids
                    for detail in detail_ids.filtered(
                        lambda r: r.collection_detail_id.id == document.id
                    ):
                        amount_cheque_collected += detail.amount
                        document.update({
                            "amount_cheque_collected": amount_cheque_collected,
                        })

    amount_cheque_collected = fields.Float(
        string="Collected Cheque Amount",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_compute_cheque_collected_amount",
    )
