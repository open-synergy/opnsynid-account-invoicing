# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = [
        "account.invoice",
        "tier.validation",
    ]
    _state_from = [
        "draft",
        "confirm"
    ]
    _state_to = [
        "open",
    ]

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("confirm", "Waiting for Approval"),
        ("proforma", "Pro-forma"),
        ("proforma2", "Pro-forma"),
        ("open", "Open"),
        ("paid", "Paid"),
        ("cancel", "Cancelled"),
    ]

    state = fields.Selection(
        string="State",
        selection=STATE_SELECTION,
        readonly=True,
        select=True,
        copy=False,
    )

    @api.model
    def _get_under_validation_exceptions(self):
        _super = super(AccountInvoice, self)
        res = _super._get_under_validation_exceptions()
        res.append("date_due")
        return res

    @api.multi
    def wkf_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())
            document.request_validation()

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
        }

    @api.multi
    def validate_tier(self):
        _super = super(AccountInvoice, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.signal_workflow("invoice_open")

    @api.multi
    def restart_validation(self):
        _super = super(AccountInvoice, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()

    @api.multi
    def action_cancel(self):
        _super = super(AccountInvoice, self)
        _super.action_cancel()
        for document in self:
            document.restart_validation()
