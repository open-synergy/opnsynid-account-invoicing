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
            if self.env.user.id == SUPERUSER_ID:
                invoice.open_ok = invoice.refund_ok = \
                    invoice.cancel_ok = invoice.restart_ok = \
                    invoice.reopen_ok = invoice.send_email_ok = \
                    invoice.proforma_ok = True
                continue

            if invoice.journal_id:
                journal = invoice.journal_id
                for policy in journal.\
                        _get_invoice_workflow_button_policy_map():
                    setattr(
                        invoice,
                        policy[0],
                        journal._get_invoice_workflow_button_policy(
                            policy[1]),
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
