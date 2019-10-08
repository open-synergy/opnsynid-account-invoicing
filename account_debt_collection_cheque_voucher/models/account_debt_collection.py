# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountDebtCollection(models.Model):
    _inherit = "account.debt_collection"

    cheque_detail_ids = fields.One2many(
        string="Cheque Receipts",
        comodel_name="account.debt_collection_cheque",
        inverse_name="debt_collection_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def _compute_allowed_journal_cheque_ids(self):
        voucher_type_id =\
            self.env.ref(
                "account_voucher_cheque.voucher_type_cheque_receipt")
        obj_voucher_type_allowed_journal =\
            self.env["account.voucher_type_allowed_journal"]

        for document in self:
            journal_ids =\
                obj_voucher_type_allowed_journal.search([
                    ("voucher_type_id", "=", voucher_type_id.id)
                ]).mapped(lambda r: r.journal_id.id)
            document.allowed_journal_cheque_ids = journal_ids

    allowed_journal_cheque_ids = fields.Many2many(
        string="Allowed Cheque Receipt Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journal_cheque_ids",
        store=False,
    )

    @api.multi
    def _prepare_cheque_receipt_data(self, document):
        self.ensure_one()

        return {
            "date_issue": document.date_issue,
            "source_bank_id": document.source_bank_id.id,
            "payee_partner_id": document.payee_partner_id.id,
        }

    @api.multi
    def _create_cheque_receipt(self):
        self.ensure_one()

        voucher_type_id =\
            self.env.ref(
                "account_voucher_cheque.voucher_type_cheque_receipt")

        obj_cheque_receipt =\
            self.env["account.cheque_receipt"]
        obj_cheque_receipt_line =\
            self.env["account.cheque_receipt_line"]

        for cheque in self.cheque_detail_ids:
            voucher_data =\
                self._prepare_receipt_voucher_data(
                    cheque, voucher_type_id)
            cheque_data =\
                self._prepare_cheque_receipt_data(cheque)
            cheque_data.update(voucher_data)
            chr = obj_cheque_receipt.create(cheque_data)
            cheque.write({
                "cheque_receipt_id": chr.id
            })
            for cheque_detail in cheque.detail_ids:
                cheque_line = obj_cheque_receipt_line.create(
                    self._prepare_receipt_voucher_line_data(
                        chr, cheque_detail))
                cheque_detail.write({
                    "cheque_receipt_line_id": cheque_line.id
                })
        return chr

    @api.multi
    def action_done(self):
        _super = super(AccountDebtCollection, self)
        result = _super.action_done()
        for document in self:
            cheque_detail_ids =\
                document.cheque_detail_ids
            detail_cheque =\
                document.cheque_detail_ids.detail_ids
            if cheque_detail_ids and detail_cheque:
                document._create_cheque_receipt()
        return result
