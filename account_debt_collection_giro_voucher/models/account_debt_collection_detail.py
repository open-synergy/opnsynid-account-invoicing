# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openerp.addons.decimal_precision as dp
from openerp import api, fields, models


class AccountDebtCollectionDetail(models.Model):
    _inherit = "account.debt_collection_detail"

    @api.multi
    def get_amount_collected_all(self):
        _super = super(AccountDebtCollectionDetail, self)
        result = _super.get_amount_collected_all()
        amount_giro_collected = self.amount_giro_collected
        result += amount_giro_collected
        return result

    @api.multi
    @api.depends(
        "amount_giro_collected",
    )
    def _compute_amount_collected(self):
        _super = super(AccountDebtCollectionDetail, self)
        _super._compute_amount_collected()

    @api.multi
    @api.depends(
        "debt_collection_id.giro_detail_ids",
        "debt_collection_id.giro_detail_ids.detail_ids",
        "debt_collection_id.giro_detail_ids.detail_ids.amount",
    )
    def _compute_giro_collected_amount(self):
        for document in self:
            amount_giro_collected = 0.0
            giro_detail_ids = document.debt_collection_id.giro_detail_ids
            if giro_detail_ids:
                for giro_detail in giro_detail_ids:
                    detail_ids = giro_detail.detail_ids
                    for detail in detail_ids.filtered(
                        lambda r: r.collection_detail_id.id == document.id
                    ):
                        amount_giro_collected += detail.amount
                        document.update(
                            {
                                "amount_giro_collected": amount_giro_collected,
                            }
                        )

    amount_giro_collected = fields.Float(
        string="Collected Giro Amount",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_compute_giro_collected_amount",
    )
