# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountDebtCollectionCheque(models.Model):
    _name = "account.debt_collection_cheque"
    _description = "Debt Collection Cheque"
    _inherit = [
        "account.debt_collection_voucher_common",
    ]

    detail_ids = fields.One2many(
        comodel_name="account.debt_collection_cheque_detail",
    )
    cheque_receipt_id = fields.Many2one(
        string="# Cheque Receipt",
        comodel_name="account.cheque_receipt",
        ondelete="cascade",
    )
    allowed_journal_ids = fields.Many2many(
        string="Allowed Cheque Receipt Journals",
        comodel_name="account.journal",
        related="debt_collection_id.allowed_journal_cheque_ids",
        store=False,
    )
    date_issue = fields.Date(
        string="Date Issued",
        required=True,
    )
    source_bank_id = fields.Many2one(
        string="Source Bank Account",
        comodel_name="res.partner.bank",
    )
    payee_partner_id = fields.Many2one(
        string="Payee",
        comodel_name="res.partner",
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_source_bank_id(self):
        obj_partner = self.env["res.partner"]
        domain = {
            "source_bank_id": [
                ("id", "=", 0),
            ]
        }
        self.source_bank_id = False
        if self.partner_id:
            commercial_partner = self.partner_id.commercial_partner_id
            criteria = [
                ("commercial_partner_id", "=", commercial_partner.id),
            ]
            partner_ids = obj_partner.search(criteria).ids
            domain["source_bank_id"] = [
                ("partner_id", "in", partner_ids),
            ]

        return {"domain": domain}

    @api.multi
    def _check_cheque_receipt_cancel(self):
        self.ensure_one()
        result = True
        obj_cheque_receipt =\
            self.env["account.cheque_receipt"]
        if self.cheque_receipt_id:
            criteria = [
                ("state", "<>", "draft"),
                ("id", "=", self.cheque_receipt_id.id)
            ]
            post_count = obj_cheque_receipt.search_count(criteria)
            if post_count > 0:
                result = False
        return result
