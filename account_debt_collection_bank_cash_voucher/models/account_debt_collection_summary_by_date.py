# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
import openerp.addons.decimal_precision as dp


class AccountDebtCollectionSummaryByDate(models.Model):
    _inherit = "account.debt_collection_summary_by_date"

    total_amount_bank_collected = fields.Float(
        string="Total Collected Bank Amount",
        digits=dp.get_precision("Account"),
    )

    total_amount_cash_collected = fields.Float(
        string="Total Collected Cash Amount",
        digits=dp.get_precision("Account"),
    )

    def _select(self):
        _super = super(AccountDebtCollectionSummaryByDate, self)
        select_str = _super._select() + """,
            SUM(a.amount_bank_collected) AS total_amount_bank_collected,
            SUM(a.amount_cash_collected) AS total_amount_cash_collected
        """
        return select_str
