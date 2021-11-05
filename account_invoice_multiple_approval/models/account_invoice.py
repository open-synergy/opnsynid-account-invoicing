# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


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
            ("open", "On Progress"),
            ("paid", "Paid"),
            ("cancel", "Cancelled"),
            ("terminate", "Terminated"),
            ("reject", "Rejected"),
        ],
        default="draft",
    )

    def action_confirm(self):
        for document in self:
            document.write({"state": "confirm"})
            document.action_request_approval()

    def action_open(self):
        for document in self:
            document.write({"state": "open"})

    def action_restart(self):
        for document in self:
            document.write({"state": "draft"})

    def action_cancel(self):
        for document in self:
            document.write({"state": "cancel"})

    def action_approve_approval(self):
        _super = super(AccountInvoice, self)
        _super.action_approve_approval()
        for document in self:
            if document.approved:
                document.action_open()
