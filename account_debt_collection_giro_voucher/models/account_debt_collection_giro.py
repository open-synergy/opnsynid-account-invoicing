# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountDebtCollectionGiro(models.Model):
    _name = "account.debt_collection_giro"
    _description = "Debt Collection Giro"
    _inherit = [
        "account.debt_collection_voucher_common",
    ]

    detail_ids = fields.One2many(
        comodel_name="account.debt_collection_giro_detail",
    )
    giro_receipt_id = fields.Many2one(
        string="# Giro Receipt",
        comodel_name="account.giro_receipt",
        ondelete="cascade",
    )
    allowed_journal_ids = fields.Many2many(
        string="Allowed Giro Receipt Journals",
        comodel_name="account.journal",
        related="debt_collection_id.allowed_journal_giro_ids",
        store=False,
    )
    date_issue = fields.Date(
        string="Date Issued",
        required=True,
    )
    date_due = fields.Date(
        string="Date Due",
        required=True,
    )
    source_bank_id = fields.Many2one(
        string="Source Bank Account",
        comodel_name="res.partner.bank",
    )
    destination_bank_id = fields.Many2one(
        string="Destination Bank Account",
        comodel_name="res.partner.bank",
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

    @api.onchange(
        "partner_id",
        "company_id",
    )
    def onchange_destination_bank_id(self):
        obj_partner = self.env["res.partner"]
        domain = {
            "destination_bank_id": [
                ("id", "=", 0),
            ]
        }
        self.source_bank_id = False
        if self.company_id and self.partner_id:
            commercial_partner = self.company_id.partner_id.\
                commercial_partner_id
            criteria = [
                ("commercial_partner_id", "=", commercial_partner.id),
            ]
            partner_ids = obj_partner.search(criteria).ids
            domain["destination_bank_id"] = [
                ("partner_id", "in", partner_ids),
            ]

        return {"domain": domain}

    @api.multi
    def _check_giro_receipt_cancel(self):
        self.ensure_one()
        result = True
        obj_giro_receipt =\
            self.env["account.giro_receipt"]
        if self.giro_receipt_id:
            criteria = [
                ("state", "not in", ["draft", "cancel"]),
                ("id", "=", self.giro_receipt_id.id)
            ]
            post_count = obj_giro_receipt.search_count(criteria)
            if post_count > 0:
                result = False
        return result
