# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = [
        "account.invoice",
        "mixin.multiple_approval",
    ]
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "Open"),
            ("paid", "Paid"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
    )

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write({"state": "confirm"})
            document.action_request_approval()

    @api.multi
    def action_open(self):
        for document in self:
            if (
                float_compare(
                    document.amount_total,
                    0.0,
                    precision_rounding=document.currency_id.rounding,
                )
                == -1
            ):
                error_msg = (
                    "You cannot validate an invoice with a negative "
                    "total amount. You should create a credit note "
                    "instead."
                )
                raise UserError(_(error_msg))
            document.action_date_assign()
            document.action_move_create()
            return document.invoice_validate()

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_draft_data())
            document._delete_attachment()
        return True

    @api.multi
    def _prepare_draft_data(self):
        return {
            "state": "draft",
            "date": False,
        }

    @api.multi
    def _delete_attachment(self):
        self.ensure_one()
        try:
            report_invoice = self.env["ir.actions.report"]._get_report_from_name(
                "account.report_invoice"
            )
        except IndexError:
            report_invoice = False
        if report_invoice and report_invoice.attachment:
            with self.env.do_in_draft():
                self.number, self.state = self.move_name, "open"
                attachment = self.env.ref(
                    "account.account_invoices"
                ).retrieve_attachment(self)
            if attachment:
                attachment.unlink()

    @api.multi
    def action_approve_approval(self):
        _super = super(AccountInvoice, self)
        _super.action_approve_approval()
        for document in self:
            if document.approved:
                document.action_open()

    @api.multi
    def action_invoice_cancel(self):
        self.action_cancel()
