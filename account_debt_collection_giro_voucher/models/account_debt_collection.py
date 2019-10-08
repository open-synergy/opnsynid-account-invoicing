# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountDebtCollection(models.Model):
    _inherit = "account.debt_collection"

    giro_detail_ids = fields.One2many(
        string="Giro Receipts",
        comodel_name="account.debt_collection_giro",
        inverse_name="debt_collection_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def _compute_allowed_journal_giro_ids(self):
        voucher_type_id =\
            self.env.ref(
                "account_voucher_giro.voucher_type_giro_receipt")
        obj_voucher_type_allowed_journal =\
            self.env["account.voucher_type_allowed_journal"]

        for document in self:
            journal_ids =\
                obj_voucher_type_allowed_journal.search([
                    ("voucher_type_id", "=", voucher_type_id.id)
                ]).mapped(lambda r: r.journal_id.id)
            document.allowed_journal_giro_ids = journal_ids

    allowed_journal_giro_ids = fields.Many2many(
        string="Allowed Giro Receipt Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journal_giro_ids",
        store=False,
    )

    @api.multi
    def _prepare_giro_receipt_data(self, document):
        self.ensure_one()

        return {
            "date_issue": document.date_issue,
            "date_due": document.date_due,
            "source_bank_id": document.source_bank_id.id,
            "destination_bank_id": document.destination_bank_id.id,
        }

    @api.multi
    def _create_giro_receipt(self):
        self.ensure_one()

        voucher_type_id =\
            self.env.ref(
                "account_voucher_giro.voucher_type_giro_receipt")

        obj_giro_receipt =\
            self.env["account.giro_receipt"]
        obj_giro_receipt_line =\
            self.env["account.giro_receipt_line"]

        for giro in self.giro_detail_ids:
            voucher_data =\
                self._prepare_receipt_voucher_data(
                    giro, voucher_type_id)
            giro_data =\
                self._prepare_giro_receipt_data(giro)
            giro_data.update(voucher_data)
            gr = obj_giro_receipt.create(giro_data)
            giro.write({
                "giro_receipt_id": gr.id
            })
            for giro_detail in giro.detail_ids:
                giro_line = obj_giro_receipt_line.create(
                    self._prepare_receipt_voucher_line_data(
                        gr, giro_detail))
                giro_detail.write({
                    "giro_receipt_line_id": giro_line.id
                })
        return gr

    @api.multi
    def action_done(self):
        _super = super(AccountDebtCollection, self)
        result = _super.action_done()
        for document in self:
            giro_detail_ids =\
                document.giro_detail_ids
            detail_giro =\
                document.giro_detail_ids.detail_ids
            if giro_detail_ids and detail_giro:
                document._create_giro_receipt()
        return result
