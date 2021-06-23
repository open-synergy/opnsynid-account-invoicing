# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    @api.depends(
        "state",
        "move_id",
        "move_id",
        "move_id.state",
        "move_id.line_id",
        "move_id.line_id.reconcile_id",
        "move_id.line_id.reconcile_partial_id",
    )
    def _compute_last_payment_info(self):
        for inv in self:
            payment_date = move_line_id = move_id = False
            if inv.move_lines:
                line = inv.move_lines.sorted(key=lambda r: r.date, reverse=True)[0]
                payment_date = line.date
                move_line_id = line.id
                move_id = line.move_id.id
            inv.last_payment_date = payment_date
            inv.last_payment_line_id = move_line_id
            inv.last_payment_move_id = move_id

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
