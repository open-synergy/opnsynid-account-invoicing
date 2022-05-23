# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountAssetAsset(models.Model):
    _name = "account.asset.asset"
    _inherit = ["account.asset.asset"]

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
            record._reverese_deferred_revenue(
                date, journal, move_prefix, line_prefix, reconcile
            )

    @api.multi
    def _reverese_deferred_revenue(
        self,
        date=False,
        journal=False,
        move_prefix=False,
        line_prefix=False,
        reconcile=False,
    ):
        self.ensure_one()
        obj_move = self.env["account.move"]

        depr_lines = self._get_deferred_revenue_line_to_be_reverse()

        if len(depr_lines) == 0:
            return False

        depr_lines.action_reverese_deferred_revenue(
            date, journal, move_prefix, line_prefix, reconcile
        )

        disposal_move_ids = self._get_disposal_moves()
        disposal_moves = obj_move.browse(disposal_move_ids)

        disposal_moves.write(
            {
                "date": date,
            }
        )

        disposal_moves.create_reversals(
            date=date,
            journal=journal,
            move_prefix=move_prefix,
            line_prefix=line_prefix,
            reconcile=reconcile,
        )

        self.depreciation_line_ids[-1].post_lines_and_close_asset()

    @api.multi
    def _get_deferred_revenue_line_to_be_reverse(self):
        self.ensure_one()

        result = False

        obj_depr_line = self.env["account.asset.depreciation.line"]

        criteria = [
            ("asset_id.id", "=", self.id),
            ("move_id", "!=", False),
        ]

        depr_lines = obj_depr_line.search(criteria)

        if len(depr_lines) > 0:
            result = depr_lines

        return result
