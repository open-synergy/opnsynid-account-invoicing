# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = [
        "account.invoice",
    ]

    @api.multi
    def invoice_line_move_line_get(self):
        _super = super(AccountInvoice, self)
        obj_line = self.env["account.invoice.line"]
        results = _super.invoice_line_move_line_get()
        for result in results:
            line = obj_line.browse(result["invl_id"])
            result.update(
                {
                    "name": line.name,
                }
            )
        return results
