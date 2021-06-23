# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountDebtCollectionBankDetail(models.Model):
    _name = "account.debt_collection_bank_detail"
    _description = "Debt Collection Bank Detail"
    _inherit = [
        "account.debt_collection_voucher_detail_common",
    ]

    collection_voucher_id = fields.Many2one(
        comodel_name="account.debt_collection_bank",
    )
    bank_receipt_line_id = fields.Many2one(
        string="# Bank Receipt Line",
        comodel_name="account.bank_receipt_line",
        ondelete="cascade",
    )
