# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountDebtCollectionType(models.Model):
    _inherit = "account.debt_collection_type"

    positive_write_off_account_id = fields.Many2one(
        string="Positive Write-Off Account",
        comodel_name="account.account",
        company_dependent=True,
    )
    negative_write_off_account_id = fields.Many2one(
        string="Negative Write-Off Account",
        comodel_name="account.account",
        company_dependent=True,
    )
