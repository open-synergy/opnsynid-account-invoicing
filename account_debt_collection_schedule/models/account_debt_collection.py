# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountDebtCollection(models.Model):
    _inherit = "account.debt_collection"

    cron_create_date = fields.Datetime(
        string="Cron Created Date",
        readonly=True,
    )
    cron_create_user_id = fields.Many2one(
        string="Cron Created By",
        comodel_name="res.users",
        readonly=True,
    )
