# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    collector_id = fields.Many2one(
        string="Collector",
        comodel_name="res.users",
    )
