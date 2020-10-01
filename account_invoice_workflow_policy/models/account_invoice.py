# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = [
        "account.invoice",
        "base.workflow_policy_object"
    ]

    @api.multi
    @api.depends(
        "journal_id",
    )
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
    reopen_ok = fields.Boolean(
        string="Can Re-Open",
        compute="_compute_policy",
        store=False,
    )
    send_email_ok = fields.Boolean(
        string="Can Send by Email",
        compute="_compute_policy",
        store=False,
    )
    proforma_ok = fields.Boolean(
        string="Can PRO-FORMA",
        compute="_compute_policy",
        store=False,
    )
