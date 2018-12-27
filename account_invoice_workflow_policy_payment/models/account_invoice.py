# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    pay_ok = fields.Boolean(
        string="Can Pay/Register Payment",
        compute="_compute_policy",
        store=False,
    )
