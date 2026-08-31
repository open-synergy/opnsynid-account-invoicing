# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = [
        "account.invoice",
        "mixin.ematerai_document",
    ]
    _ematerai_document_create_page = True

    @api.multi
    def action_cancel(self):
        _super = super(AccountInvoice, self)
        _super.action_cancel()

        for document in self:
            if document.ematerai_document_ids:
                document.ematerai_document_ids.unlink()
