# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountJournal(models.Model):
    _inherit = "account.journal"

    invoice_open_group_ids = fields.Many2many(
        string="Allowed to Validate",
        comodel_name="res.groups",
        relation="rel_invoice_open_groups",
        column1="journal_id",
        column2="group_id",
    )

    invoice_refund_group_ids = fields.Many2many(
        string="Allowed to Refund",
        comodel_name="res.groups",
        relation="rel_invoice_refund_groups",
        column1="journal_id",
        column2="group_id",
    )

    invoice_cancel_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        relation="rel_invoice_cancel_groups",
        column1="journal_id",
        column2="group_id",
    )

    invoice_restart_group_ids = fields.Many2many(
        string="Allowed to Set To Draft",
        comodel_name="res.groups",
        relation="rel_invoice_restart_groups",
        column1="journal_id",
        column2="group_id",
    )

    invoice_reopen_group_ids = fields.Many2many(
        string="Allowed to Re-Open",
        comodel_name="res.groups",
        relation="rel_invoice_reopen_groups",
        column1="journal_id",
        column2="group_id",
    )

    invoice_send_email_group_ids = fields.Many2many(
        string="Allowed to Send by Email",
        comodel_name="res.groups",
        relation="rel_invoice_send_email_groups",
        column1="journal_id",
        column2="group_id",
    )

    invoice_proforma_group_ids = fields.Many2many(
        string="Allowed to Pro-Forma",
        comodel_name="res.groups",
        relation="rel_invoice_proforma_groups",
        column1="journal_id",
        column2="group_id",
    )

    @api.model
    def _get_invoice_workflow_button_policy_map(self):
        return [
            ("open_ok", "invoice_open_group_ids"),
            ("refund_ok", "invoice_refund_group_ids"),
            ("cancel_ok", "invoice_cancel_group_ids"),
            ("restart_ok", "invoice_restart_group_ids"),
            ("reopen_ok", "invoice_reopen_group_ids"),
            ("send_email_ok", "invoice_send_email_group_ids"),
            ("proforma_ok", "invoice_proforma_group_ids"),
        ]

    @api.multi
    def _get_invoice_workflow_button_policy(self, policy_field):
        self.ensure_one()
        result = False
        button_group_ids = []
        user = self.env.user
        group_ids = user.groups_id.ids

        button_group_ids += getattr(
            self, policy_field).ids

        if not button_group_ids:
            result = True
        else:
            if (set(button_group_ids) & set(group_ids)):
                result = True
        return result
