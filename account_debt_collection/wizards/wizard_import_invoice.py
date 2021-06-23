# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountDebtCollectionImportInvoice(models.TransientModel):
    _name = "account.debt_collection_import_invoice"
    _description = "Debt Collection Import Invoice"

    @api.model
    def _default_collection_id(self):
        active_id = self.env.context.get("active_id", False)
        return active_id

    collection_id = fields.Many2one(
        string="Collection",
        comodel_name="account.debt_collection",
        default=lambda self: self._default_collection_id(),
    )

    allowed_invoice_ids = fields.Many2many(
        string="Invoices",
        comodel_name="account.invoice",
        related="collection_id.allowed_invoice_ids",
        store=False,
    )

    invoice_ids = fields.Many2many(
        string="Invoices",
        comodel_name="account.invoice",
        relation="rel_debt_col_import_2_invoice",
        column1="wizard_id",
        column2="invoice_id",
    )

    @api.onchange(
        "collection_id",
    )
    def onchange_invoice_ids(self):
        if self.collection_id:
            self.invoice_ids = self.collection_id.allowed_invoice_specific_ids.ids

    @api.multi
    def action_import_invoice(self):
        self.ensure_one()
        obj_debt_collection = self.env["account.debt_collection"]
        obj_debt_collection_detail = self.env["account.debt_collection_detail"]
        active_id = self.env.context.get("active_id", False)

        criteria = [("id", "=", active_id)]
        debt_collection = obj_debt_collection.search(criteria)
        if debt_collection.detail_ids:
            debt_collection.detail_ids.unlink()

        for invoice in self.invoice_ids:
            detail_id = obj_debt_collection_detail.create(
                {
                    "debt_collection_id": active_id,
                    "invoice_id": invoice.id,
                }
            )
            detail_id.onchange_amount_due()
            invoice.write({"debt_collection_detail_id": detail_id.id})
