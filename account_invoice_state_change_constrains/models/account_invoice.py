# Copyright 2021 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = [
        "account.invoice",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    @api.onchange(
        "user_id",
    )
    def onchange_status_check_template_id(self):
        self.status_check_template_id = False
        if self.user_id:
            template_id = self._get_template_status_check()
            self.status_check_template_id = template_id

    @api.model
    def create(self, values):
        _super = super(AccountInvoice, self)
        result = _super.create(values)
        status_check_template_id = result._get_template_status_check()
        result.write(
            {
                "status_check_template_id": status_check_template_id,
            }
        )
        result.create_status_check_ids()
        result.onchange_state_change_constrain_template_id()
        return result
