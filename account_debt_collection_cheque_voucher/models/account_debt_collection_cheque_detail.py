# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountDebtCollectionChequeDetail(models.Model):
    _name = "account.debt_collection_cheque_detail"
    _description = "Debt Collection Cheque Detail"
    _inherit = [
        "account.debt_collection_voucher_detail_common",
    ]

    collection_voucher_id = fields.Many2one(
        comodel_name="account.debt_collection_cheque",
    )
    cheque_receipt_line_id = fields.Many2one(
        string="# Cheque Receipt Line",
        comodel_name="account.cheque_receipt_line",
    )
