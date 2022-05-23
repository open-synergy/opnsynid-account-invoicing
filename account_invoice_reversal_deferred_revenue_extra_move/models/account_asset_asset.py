# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountAssetAsset(models.Model):
    _name = "account.asset.asset"
    _inherit = ["account.asset.asset"]

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
        _super = super(AccountAssetAsset, self)
        _super._reverese_deferred_revenue(
            date, journal, move_prefix, line_prefix, reconcile
        )

        if self.extra_move_id:
            self.extra_move_id.create_reversals(
                date=date,
                journal=journal,
                move_prefix=move_prefix,
                line_prefix=line_prefix,
                reconcile=reconcile,
            )
