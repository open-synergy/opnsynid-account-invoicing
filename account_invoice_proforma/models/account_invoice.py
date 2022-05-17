# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ["account.invoice"]

    @api.depends(
        "proforma_number",
    )
    def _compute_proforma(self):
        for record in self:
            result = True
            if not record.proforma_number:
                result = False
            record.proforma = result

    proforma = fields.Boolean(
        string="Proforma",
        compute="_compute_proforma",
        store=True,
    )
    proforma_number = fields.Char(
        string="# Proforma",
    )

    @api.multi
    def action_generate_proforma_number(self):
        for record in self:
            record._generate_proforma_invoice()

    @api.multi
    def _generate_proforma_invoice(self):
        self.ensure_one()
        if not self.proforma_number:
            self.write(
                {
                    "proforma_number": self._get_proforma_number(),
                }
            )

    @api.multi
    def _get_proforma_number(self):
        self.ensure_one()
        sequence = self._get_proforma_sequence()
        error_msg = """No proforma sequence

        Choose proforma sequence on journal configuration"""
        if not sequence:
            raise ValidationError(_(error_msg))

        date_invoice = self.date_invoice and self.date_invoice or fields.Date.today()

        ctx = {"ir_sequence_date": date_invoice}
        result = sequence.with_context(ctx).next_by_id()
        return result

    @api.multi
    def _get_proforma_sequence(self):
        self.ensure_one()
        return self.journal_id and self.journal_id.proforma_sequence_id or False
