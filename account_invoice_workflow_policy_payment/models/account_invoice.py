# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    pay_ok = fields.Boolean(
        string="Can Pay/Register Payment",
        compute="_compute_policy",
        store=False,
    )
