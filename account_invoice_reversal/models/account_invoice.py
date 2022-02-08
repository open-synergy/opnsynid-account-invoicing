# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice"]

    reversal_id = fields.Many2one(
        string="Reversal Entry",
        comodel_name="account.move",
        related="move_id.reversal_id",
        store=True,
        readonly=False,
    )
