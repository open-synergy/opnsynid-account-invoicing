# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice"]

    @api.depends(
        "state",
        "reversal_id",
    )
    def _compute_paid_status(self):
        for record in self:
            result = False
            if record.state == "paid" and record.reversal_id:
                result = "reverse"
            elif record.state == "paid" and not record.reversal_id:
                result = "paid"
            record.paid_status = result

    reversal_id = fields.Many2one(
        string="Reversal Entry",
        comodel_name="account.move",
        related="move_id.reversal_id",
        store=True,
        readonly=False,
    )
    paid_status = fields.Selection(
        string="Paid Status",
        selection=[
            ("paid", "Paid"),
            ("reverse", "Reversed"),
        ],
        compute="_compute_paid_status",
        store=True,
    )
