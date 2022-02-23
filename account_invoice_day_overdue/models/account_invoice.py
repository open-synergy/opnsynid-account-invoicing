# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice"]

    @api.depends(
        "move_id",
        "move_id.line_ids",
        "move_id.line_ids.days_overdue",
    )
    def _compute_days_overdue(self):
        obj_ml = self.env["account.move.line"]
        for record in self:
            result = 0
            if record.move_id:
                criteria = [
                    ("move_id", "=", record.move_id.id),
                    ("account_id", "=", record.account_id.id),
                ]
                mls = obj_ml.search(criteria, limit=1)
                if len(mls) == 1:
                    result = mls[0].days_overdue
            record.days_overdue = result

    days_overdue = fields.Integer(
        string="Days Overdue",
        compute="_compute_days_overdue",
        store=True,
    )
