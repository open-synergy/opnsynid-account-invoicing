# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class AccountDebtCollectionVoucherCommon(models.AbstractModel):
    _name = "account.debt_collection_voucher_common"
    _description = "Abstract Model for Debt Collection Voucher"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self._default_company_id(),
    )

    @api.model
    def _default_collection_id(self):
        active_id =\
            self.env.context.get("debt_collection_id", False)
        return active_id

    debt_collection_id = fields.Many2one(
        string="# Collection",
        comodel_name="account.debt_collection",
        default=lambda self: self._default_collection_id(),
        required=True,
        readonly=True
    )

    @api.model
    def _default_date(self):
        return fields.Datetime.now()

    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: self._default_date(),
    )

    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
    )

    period_id = fields.Many2one(
        string="Period",
        comodel_name="account.period",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
    )

    @api.multi
    @api.depends(
        "detail_ids.amount"
    )
    def _compute_amount(self):
        for document in self:
            amount = 0.0
            for detail in document.detail_ids:
                amount += detail.amount
            document.update({
                "amount": amount,
            })

    amount = fields.Float(
        string="Amount",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_compute_amount",
    )
    amount_real = fields.Float(
        string="Real Amount",
        digits=dp.get_precision("Account"),
        required=True,
        default=0.0,
    )

    reference = fields.Char(
        string="Reference",
        required=True,
        default="/",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="account.debt_collection_voucher_detail_common",
        inverse_name="collection_voucher_id",
    )
    allowed_partner_ids = fields.Many2many(
        string="Allowed Partners",
        comodel_name="res.partner",
        related="debt_collection_id.allowed_partner_ids",
        store=False,
    )

    @api.multi
    @api.onchange("date")
    def onchange_period_id(self):
        self.period_id = self.env[
            "account.period"].find(self.date).id

    @api.multi
    def _get_write_off_account(self):
        self.ensure_one()

        collection = self.debt_collection_id
        collection_type = collection.collection_type_id
        result = False

        if self.amount_real > self.amount:
            result = collection_type.positive_write_off_account_id
        elif self.amount_real < self.amount:
            result = collection_type.negative_write_off_account_id

        return result
