# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    @api.depends(
        "payment_move_line_ids",
    )
    def _compute_last_payment_info(self):
        for document in self:
            payment_date = move_line_id = move_id = False
            if document.payment_move_line_ids:
                move_line = document.payment_move_line_ids.sorted(
                    key=lambda r: r.date, reverse=True
                )[0]
                payment_date = move_line.date
                move_line_id = move_line.id
                move_id = move_line.move_id.id
            document.last_payment_date = payment_date
            document.last_payment_line_id = move_line_id
            document.last_payment_move_id = move_id

    last_payment_date = fields.Date(
        string="Last Payment Date",
        compute="_compute_last_payment_info",
        store=True,
        readonly=True,
    )

    last_payment_line_id = fields.Many2one(
        string="Last Payment Move Line",
        comodel_name="account.move.line",
        compute="_compute_last_payment_info",
        store=True,
        readonly=True,
    )

    last_payment_move_id = fields.Many2one(
        string="Last Payment Move",
        comodel_name="account.move",
        compute="_compute_last_payment_info",
        store=True,
        readonly=True,
    )
