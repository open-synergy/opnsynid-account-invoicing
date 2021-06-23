# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountDebtCollectionCash(models.Model):
    _name = "account.debt_collection_cash"
    _description = "Debt Collection Cash"
    _inherit = [
        "account.debt_collection_voucher_common",
    ]

    detail_ids = fields.One2many(
        comodel_name="account.debt_collection_cash_detail",
    )
    cash_receipt_id = fields.Many2one(
        string="# Cash Receipt",
        comodel_name="account.cash_receipt",
        ondelete="cascade",
    )
    allowed_journal_ids = fields.Many2many(
        string="Allowed Cash Receipt Journals",
        comodel_name="account.journal",
        related="debt_collection_id.allowed_journal_cr_ids",
        store=False,
    )

    @api.multi
    def _check_cash_receipt_cancel(self):
        self.ensure_one()
        result = True
        obj_cash_receipt = self.env["account.cash_receipt"]
        if self.cash_receipt_id:
            criteria = [
                ("state", "not in", ["draft", "cancel"]),
                ("id", "=", self.cash_receipt_id.id),
            ]
            post_count = obj_cash_receipt.search_count(criteria)
            if post_count > 0:
                result = False
        return result
