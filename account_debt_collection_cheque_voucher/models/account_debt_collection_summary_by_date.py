# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
import openerp.addons.decimal_precision as dp


class AccountDebtCollectionSummaryByDate(models.Model):
    _inherit = "account.debt_collection_summary_by_date"

    total_amount_cheque_collected = fields.Float(
        string="Total Collected Cheque Amount",
        digits=dp.get_precision("Account"),
    )

    def _select(self):
        _super = super(AccountDebtCollectionSummaryByDate, self)
        select_str = _super._select() + """,
            SUM(a.amount_cheque_collected) AS total_amount_cheque_collected
        """
        return select_str
