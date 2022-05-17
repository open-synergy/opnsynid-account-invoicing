# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountJournal(models.Model):
    _name = "account.journal"
    _inherit = [
        "account.journal",
    ]

    proforma_sequence_id = fields.Many2one(
        string="Proforma Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
