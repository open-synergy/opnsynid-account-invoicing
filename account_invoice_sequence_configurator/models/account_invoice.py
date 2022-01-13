# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = [
        "account.invoice",
        "base.sequence_document",
    ]

    @api.multi
    def action_move_create(self):
        _super = super(AccountInvoice, self)
        ctx = self.env.context.copy()
        for document in self:
            ctx.update(
                {
                    "ir_sequence_date": document.date_invoice,
                }
            )
            sequence = document.with_context(ctx)._create_sequence()
            document.write({"internal_number": sequence})
        return _super.action_move_create()
