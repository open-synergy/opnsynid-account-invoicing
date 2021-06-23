# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    line_summary_ids = fields.One2many(
        string="Invoice Line Summary",
        comodel_name="account.invoice_line_summary",
        inverse_name="invoice_id",
    )
