# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    debt_collection_detail_id = fields.Many2one(
        string="# A/R Collection Detail",
        comodel_name="account.debt_collection_detail",
    )

    @api.depends("debt_collection_detail_id", "debt_collection_detail_id.invoice_id")
    @api.multi
    def _compute_debt_collection_ok(self):
        for document in self:
            document.debt_collection_ok = False
            if document.debt_collection_detail_id:
                document.debt_collection_ok = True

    debt_collection_ok = fields.Boolean(
        string="Used In A/R Collection",
        compute="_compute_debt_collection_ok",
        store=True,
        readonly=True,
    )

    @api.multi
    def _check_debt_collection_ok(self):
        self.ensure_one()
        result = False
        if self.debt_collection_ok:
            result = True
        return result

    @api.multi
    def action_cancel(self):
        _super = super(AccountInvoice, self)
        result = _super.action_cancel()
        msg = _("You cannot cancel invoice which used in A/R Collection")
        for document in self:
            if document._check_debt_collection_ok():
                raise UserError(msg)
        return result
