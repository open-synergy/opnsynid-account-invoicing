# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountJournal(models.Model):
    _inherit = "account.journal"

    invoice_pay_group_ids = fields.Many2many(
        string="Allowed to Pay/Register Payment",
        comodel_name="res.groups",
        relation="rel_invoice_pay_groups",
        column1="journal_id",
        column2="group_id",
    )

    @api.model
    def _get_invoice_workflow_button_policy_map(self):
        _super = super(AccountJournal, self)
        result = _super._get_invoice_workflow_button_policy_map()
        result += [
            ("pay_ok", "invoice_pay_group_ids"),
        ]
        return result
