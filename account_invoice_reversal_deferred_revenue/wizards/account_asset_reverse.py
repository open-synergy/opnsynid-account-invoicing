# Copyright 2011 Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2012-2013 Guewen Baconnier (Camptocamp)
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMoveReverse(models.TransientModel):
    _name = "account_asset_reverse"
    _description = "Reverse Deferred Revenue"

    date = fields.Date(
        string="Reversal Date",
        required=True,
        help="Enter the date of the reversal account entries. "
        "By default, Odoo proposes the same date of the move to reverse.",
    )
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Reversal Journal",
        help="Enter the journal of the reversal account entries. "
        "If empty, Odoo uses the same journal of the move to reverse.",
    )
    move_prefix = fields.Char(
        string="Entries Ref. Prefix",
        help="Prefix that will be added to the 'Ref' of the reversal account "
        "entries. If empty, Odoo uses the Ref of the move to reverse. "
        "(NOTE: A space is added after the prefix).",
    )
    line_prefix = fields.Char(
        string="Items Name Prefix",
        help="Prefix that will be added to the 'Name' of the reversal account "
        "entrie items. If empty, Odoo uses the same name of the move "
        "line to reverse. (NOTE: A space is added after the prefix).",
    )
    reconcile = fields.Boolean(
        string="Reconcile",
        default=True,
        help="Mark this if you want to reconcile items of both moves.",
    )

    @api.multi
    def action_reverse(self):
        deferred_revenue_ids = self.env.context.get("active_ids", [])
        deferred_revenues = self.env["account.asset.asset"].browse(deferred_revenue_ids)
        deferred_revenues.action_reverese_deferred_revenue(
            date=self.date,
            journal=self.journal_id,
            move_prefix=self.move_prefix,
            line_prefix=self.line_prefix,
            reconcile=self.reconcile,
        )
