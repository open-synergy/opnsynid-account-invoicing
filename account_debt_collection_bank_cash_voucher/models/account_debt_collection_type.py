# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountDebtCollectionType(models.Model):
    _inherit = "account.debt_collection_type"

    autopost_bank_receipt = fields.Boolean(string="Auto Post Bank Receipt")
    autopost_cash_receipt = fields.Boolean(string="Auto Post Cash Receipt")
