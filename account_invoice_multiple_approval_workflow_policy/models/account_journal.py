# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    invoice_confim_group_ids = fields.Many2many(
        string="Allowed to Confirm",
        comodel_name="res.groups",
        relation="rel_invoice_confirm_groups",
        column1="journal_id",
        column2="group_id",
    )
    invoice_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval",
        comodel_name="res.groups",
        relation="rel_invoice_restart_approval_groups",
        column1="type_id",
        column2="group_id",
    )
