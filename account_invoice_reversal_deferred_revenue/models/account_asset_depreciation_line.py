# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountAssetDepreciationLine(models.Model):
    _name = "account.asset.depreciation.line"
    _inherit = ["account.asset.depreciation.line"]

    @api.multi
    def action_reverese_deferred_revenue(
        self,
        date=False,
        journal=False,
        move_prefix=False,
        line_prefix=False,
        reconcile=False,
    ):
        for record in self:
            record._reverse_move(date, journal, move_prefix, line_prefix, reconcile)
            record.post_lines_and_close_asset()

    @api.multi
    def _reverse_move(
        self,
        date=False,
        journal=False,
        move_prefix=False,
        line_prefix=False,
        reconcile=False,
    ):
        self.ensure_one()

        self.move_id.create_reversals(
            date, journal, move_prefix, line_prefix, reconcile
        )
