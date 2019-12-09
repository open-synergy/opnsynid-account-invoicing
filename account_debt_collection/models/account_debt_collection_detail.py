# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class AccountDebtCollectionDetail(models.Model):
    _name = "account.debt_collection_detail"
    _description = "Debt Collection Details"

    @api.multi
    @api.depends(
        "invoice_id",
    )
    def _compute_partner_id(self):
        for document in self:
            document.partner_id = document.invoice_id.partner_id.\
                commercial_partner_id.id

    name = fields.Char(
        string="Description",
        default="/",
    )
    debt_collection_id = fields.Many2one(
        string="# Collection",
        comodel_name="account.debt_collection",
        required=True,
        ondelete="cascade",
    )
    invoice_id = fields.Many2one(
        string="Invoice",
        comodel_name="account.invoice",
        readonly="True",
    )
    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        compute="_compute_partner_id",
        store=True,
    )
    amount_invoice = fields.Float(
        string="Invoice Amount",
        related="invoice_id.amount_total",
    )
    amount_due = fields.Float(
        string="Amount Due",
        digits=dp.get_precision("Account"),
        readonly="True",
        default=0.0,
    )
    date_invoice = fields.Date(
        string="Invoice Date",
        related="invoice_id.date_invoice",
    )
    date_due = fields.Date(
        string="Invoice Due",
        related="invoice_id.date_due",
    )

    @api.multi
    def get_amount_collected_all(self):
        result = 0.0
        return result

    @api.multi
    def _compute_amount_collected(self):
        for document in self:
            amount_collected =\
                document.get_amount_collected_all()
            document.amount_collected += amount_collected

    amount_collected = fields.Float(
        string="Collected Amount",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_compute_amount_collected",
    )

    @api.multi
    def _compute_state(self):
        for document in self:
            document.state = \
                document.debt_collection_id.state

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        readonly=True,
        compute="_compute_state",
        store=False,
    )

    @api.multi
    @api.onchange(
        "invoice_id"
    )
    def onchange_amount_due(self):
        if self.invoice_id:
            self.amount_due =\
                self.invoice_id.residual

    @api.multi
    def _get_name(self):
        result = False
        if self.invoice_id:
            name = "Collection [%s]" % (self.invoice_id.number)
            result = name
        return result

    @api.model
    def create(self, values):
        _super = super(AccountDebtCollectionDetail, self)
        result = _super.create(values)
        name = result._get_name()
        if name:
            result.write({
                "name": name,
            })
        return result
