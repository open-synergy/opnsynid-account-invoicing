# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


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
        voucher_type_id = self.env.ref(
            "account_voucher_cheque.voucher_type_cheque_receipt"
        )
        obj_voucher_type_allowed_journal = self.env[
            "account.voucher_type_allowed_journal"
        ]

        for document in self:
            journal_ids = obj_voucher_type_allowed_journal.search(
                [("voucher_type_id", "=", voucher_type_id.id)]
            ).mapped(lambda r: r.journal_id.id)
            document.allowed_journal_cheque_ids = journal_ids

    allowed_journal_cheque_ids = fields.Many2many(
        string="Allowed Cheque Receipt Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journal_cheque_ids",
        store=False,
    )

    @api.multi
    def action_cancel(self):
        _super = super(AccountDebtCollection, self)
        result = _super.action_cancel()
        for document in self:
            for cheque_detail in document.cheque_detail_ids:
                if not cheque_detail._check_cheque_receipt_cancel():
                    msg = _("Cheque Receipts must be on <Draft> state")
                    raise UserError(msg)
                cheque_detail.cheque_receipt_id.unlink()
            document.cheque_detail_ids.unlink()
        return result

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

        voucher_type_id = self.env.ref(
            "account_voucher_cheque.voucher_type_cheque_receipt"
        )

        obj_cheque_receipt = self.env["account.cheque_receipt"]
        obj_cheque_receipt_line = self.env["account.cheque_receipt_line"]

        if self.cheque_detail_ids:
            for cheque in self.cheque_detail_ids:
                if cheque.detail_ids:
                    voucher_data = self._prepare_receipt_voucher_data(
                        cheque, voucher_type_id
                    )
                    cheque_data = self._prepare_cheque_receipt_data(cheque)
                    cheque_data.update(voucher_data)
                    chr = obj_cheque_receipt.create(cheque_data)
                    cheque.write({"cheque_receipt_id": chr.id})
                    for cheque_detail in cheque.detail_ids:
                        cheque_line = obj_cheque_receipt_line.create(
                            self._prepare_receipt_voucher_line_data(chr, cheque_detail)
                        )
                        cheque_detail.write({"cheque_receipt_line_id": cheque_line.id})
        return True

    @api.multi
    def action_done(self):
        _super = super(AccountDebtCollection, self)
        result = _super.action_done()
        for document in self:
            document._create_cheque_receipt()
        return result

    @api.multi
    def _get_cheque_receipts(self):
        return self.mapped("cheque_detail_ids.cheque_receipt_id")

    @api.multi
    def _get_action_cheque_receipt(self):
        action = self.env.ref(
            "account_voucher_cheque." "account_cheque_receipt_action"
        ).read()[0]
        return action

    @api.multi
    def action_view_cheque_receipts(self):
        self.ensure_one()
        receipts = self._get_cheque_receipts()
        action = self._get_action_cheque_receipt()

        if len(receipts) > 0:
            action["domain"] = [("id", "in", receipts.ids)]
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action
