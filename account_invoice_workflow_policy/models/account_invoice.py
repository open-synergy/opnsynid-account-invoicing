# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, SUPERUSER_ID


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    @api.depends(
        "journal_id",
    )
    def _compute_policy(self):
        for invoice in self:
            journal = invoice.journal_id
            if journal:
                for policy in journal.\
                        _get_invoice_workflow_button_policy_map():
                    if self.env.user.id == SUPERUSER_ID:
                        result = True
                    else:
                        result = journal.\
                            _get_invoice_workflow_button_policy(
                                policy[1])
                    setattr(
                        invoice,
                        policy[0],
                        result,
                    )

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
