# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


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
    def action_cancel(self):
        _super = super(AccountDebtCollection, self)
        result = _super.action_cancel()
        for document in self:
            for giro_detail in document.giro_detail_ids:
                if not giro_detail._check_giro_receipt_cancel():
                    msg = _("Please Cancel All giro Receipts")
                    raise UserError(msg)
                ctx = {
                    "force_unlink": True
                }
                giro_detail.giro_receipt_id.with_context(ctx).unlink()
            document.giro_detail_ids.unlink()
        return result

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

        if self.giro_detail_ids:
            for giro in self.giro_detail_ids:
                if giro.detail_ids:
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
        return True

    @api.multi
    def action_done(self):
        _super = super(AccountDebtCollection, self)
        result = _super.action_done()
        for document in self:
            document._create_giro_receipt()
        return result

    @api.multi
    def _get_giro_receipts(self):
        return self.mapped("giro_detail_ids.giro_receipt_id")

    @api.multi
    def _get_action_giro_receipt(self):
        action =\
            self.env.ref(
                'account_voucher_giro.'
                'account_giro_receipt_action').read()[0]
        return action

    @api.multi
    def action_view_giro_receipts(self):
        receipts = self._get_giro_receipts()
        action = self._get_action_giro_receipt()

        if len(receipts) > 0:
            action['domain'] = [('id', 'in', receipts.ids)]
            action['context'] = [('id', 'in', receipts.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
