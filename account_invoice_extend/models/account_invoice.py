# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    state = fields.Selection(
    	selection_add=[
    		("confirm", "Confirm")
		]
    )
