# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountDebtCollection(models.Model):
    _inherit = "account.debt_collection"

    bank_detail_ids = fields.One2many(
        string="Bank Receipts",
        comodel_name="account.debt_collection_bank",
        inverse_name="debt_collection_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    cash_detail_ids = fields.One2many(
        string="Cash Receipts",
        comodel_name="account.debt_collection_cash",
        inverse_name="debt_collection_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def _compute_allowed_journal_br_ids(self):
        voucher_type_id =\
            self.env.ref(
                "account_voucher_bank_cash.voucher_type_bank_receipt")
        obj_voucher_type_allowed_journal =\
            self.env["account.voucher_type_allowed_journal"]

        for document in self:
            journal_ids =\
                obj_voucher_type_allowed_journal.search([
                    ("voucher_type_id", "=", voucher_type_id.id)
                ]).mapped(lambda r: r.journal_id.id)
            document.allowed_journal_br_ids = journal_ids

    allowed_journal_br_ids = fields.Many2many(
        string="Allowed Bank Receipt Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journal_br_ids",
        store=False,
    )

    @api.multi
    def _compute_allowed_journal_cr_ids(self):
        voucher_type_id =\
            self.env.ref(
                "account_voucher_bank_cash.voucher_type_cash_receipt")
        obj_voucher_type_allowed_journal =\
            self.env["account.voucher_type_allowed_journal"]

        for document in self:
            journal_ids =\
                obj_voucher_type_allowed_journal.search([
                    ("voucher_type_id", "=", voucher_type_id.id)
                ]).mapped(lambda r: r.journal_id.id)
            document.allowed_journal_cr_ids = journal_ids

    allowed_journal_cr_ids = fields.Many2many(
        string="Allowed Cash Receipt Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journal_cr_ids",
        store=False,
    )

    @api.multi
    def _create_bank_receipt(self):
        self.ensure_one()

        voucher_type_id =\
            self.env.ref(
                "account_voucher_bank_cash.voucher_type_bank_receipt")

        obj_bank_receipt =\
            self.env["account.bank_receipt"]
        obj_bank_receipt_line =\
            self.env["account.bank_receipt_line"]

        for bank in self.bank_detail_ids:
            br = obj_bank_receipt.create(
                self._prepare_receipt_voucher_data(
                    bank, voucher_type_id))
            bank.write({
                "bank_receipt_id": br.id
            })
            for bank_detail in bank.detail_ids:
                br_line = obj_bank_receipt_line.create(
                    self._prepare_receipt_voucher_line_data(
                        br, bank_detail))
                bank_detail.write({
                    "bank_receipt_line_id": br_line.id
                })
        return br

    @api.multi
    def _create_cash_receipt(self):
        self.ensure_one()

        voucher_type_id =\
            self.env.ref(
                "account_voucher_bank_cash.voucher_type_cash_receipt")

        obj_cash_receipt =\
            self.env["account.cash_receipt"]
        obj_cash_receipt_line =\
            self.env["account.cash_receipt_line"]

        for cash in self.cash_detail_ids:
            cr = obj_cash_receipt.create(
                self._prepare_receipt_voucher_data(
                    cash, voucher_type_id))
            cash.write({
                "cash_receipt_id": cr.id
            })
            for cash_detail in cash.detail_ids:
                cr_line = obj_cash_receipt_line.create(
                    self._prepare_receipt_voucher_line_data(
                        cr, cash_detail))
                cash_detail.write({
                    "cash_receipt_line_id": cr_line.id
                })
        return cr

    @api.multi
    def action_done(self):
        _super = super(AccountDebtCollection, self)
        result = _super.action_done()
        for document in self:
            bank_detail_ids =\
                document.bank_detail_ids
            detail_bank =\
                document.bank_detail_ids.detail_ids
            if bank_detail_ids and detail_bank:
                document._create_bank_receipt()

            cash_detail_ids =\
                document.cash_detail_ids
            detail_cash =\
                document.cash_detail_ids.detail_ids
            if cash_detail_ids and detail_cash:
                document._create_cash_receipt()
        return result
