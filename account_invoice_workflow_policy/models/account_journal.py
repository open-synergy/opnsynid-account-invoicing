# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


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
