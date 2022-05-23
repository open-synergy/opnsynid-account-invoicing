# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["account.move"]

    @api.multi
    def create_reversals(
        self,
        date=False,
        journal=False,
        move_prefix=False,
        line_prefix=False,
        reconcile=False,
    ):
        _super = super(AccountMove, self)
        result = _super.create_reversals(
            date=date,
            journal=journal,
            move_prefix=move_prefix,
            line_prefix=line_prefix,
            reconcile=reconcile,
        )
        for move in self:
            move._reverse_deferred_revenue(
                date, journal, move_prefix, line_prefix, reconcile
            )
        return result

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

        invoices = self._get_deferred_revenue_invoice()

        if not invoices:
            return True

        invoices.action_reverese_deferred_revenue(
            date, journal, move_prefix, line_prefix, reconcile
        )

    @api.multi
    def _get_deferred_revenue_invoice(self):
        obj_invoice = self.env["account.invoice"]

        criteria = [
            ("move_id", "=", self.id),
            ("type", "=", "out_invoice"),
        ]

        invoices = obj_invoice.search(criteria)

        if len(invoices) > 0:
            return invoices
        return False
