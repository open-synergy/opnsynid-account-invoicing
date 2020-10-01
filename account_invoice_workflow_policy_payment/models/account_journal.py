# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    invoice_pay_group_ids = fields.Many2many(
        string="Allowed to Pay/Register Payment",
        comodel_name="res.groups",
        relation="rel_invoice_pay_groups",
        column1="journal_id",
        column2="group_id",
    )
