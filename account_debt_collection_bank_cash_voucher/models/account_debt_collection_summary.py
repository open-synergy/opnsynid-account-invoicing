# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openerp.addons.decimal_precision as dp
from openerp import fields, models


class AccountDebtCollectionDetailSummary(models.Model):
    _inherit = "account.debt_collection_detail_summary"

    total_amount_bank_collected = fields.Float(
        string="Total Collected Bank Amount",
        digits=dp.get_precision("Account"),
    )

    total_amount_cash_collected = fields.Float(
        string="Total Collected Cash Amount",
        digits=dp.get_precision("Account"),
    )

    def _select(self):
        _super = super(AccountDebtCollectionDetailSummary, self)
        select_str = (
            _super._select()
            + """,
            SUM(a.amount_bank_collected) AS total_amount_bank_collected,
            SUM(a.amount_cash_collected) AS total_amount_cash_collected
        """
        )
        return select_str
