# Copyright 2021 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice", "mixin.policy"]

    def _compute_policy(self):
        _super = super(AccountInvoice, self)
        _super._compute_policy()

    open_ok = fields.Boolean(
        string="Can Validate",
        compute="_compute_policy",
        store=False,
    )
    refund_ok = fields.Boolean(
        string="Can Refund",
        compute="_compute_policy",
        store=False,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
    )
    restart_ok = fields.Boolean(
        string="Can Set To Draft",
        compute="_compute_policy",
        store=False,
    )
    send_email_ok = fields.Boolean(
        string="Can Send by Email",
        compute="_compute_policy",
        store=False,
    )
    payment_ok = fields.Boolean(
        string="Can Register Payment",
        compute="_compute_policy",
        store=False,
    )
    print_ok = fields.Boolean(
        string="Can Print Invoice",
        compute="_compute_policy",
        store=False,
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
        store=False,
    )
    reject_ok = fields.Boolean(
        string="Can Reject",
        compute="_compute_policy",
        store=False,
    )

    @api.onchange(
        "journal_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_id()
        for document in self:
            document.policy_template_id = template_id
