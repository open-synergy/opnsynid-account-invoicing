# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice"]

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
            record._reverse_deferred_revenue(
                date, journal, move_prefix, line_prefix, reconcile
            )

    @api.multi
    def _reverse_deferred_revenue(
        self,
        date=False,
        journal=False,
        move_prefix=False,
        line_prefix=False,
        reconcile=False,
    ):
        self.ensure_one()

        obj_asset = self.env["account.asset.asset"]

        criteria = [("invoice_id.id", "=", self.id), ("active", "=", True)]

        assets = obj_asset.search(criteria)

        if len(assets) == 0:
            return False

        assets.action_reverese_deferred_revenue(
            date, journal, move_prefix, line_prefix, reconcile
        )
