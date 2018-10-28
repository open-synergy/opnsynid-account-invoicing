# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["confirm"]
