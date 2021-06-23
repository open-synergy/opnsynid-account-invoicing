# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


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
        voucher_type_id = self.env.ref(
            "account_voucher_bank_cash.voucher_type_bank_receipt"
        )
        obj_voucher_type_allowed_journal = self.env[
            "account.voucher_type_allowed_journal"
        ]

        for document in self:
            journal_ids = obj_voucher_type_allowed_journal.search(
                [("voucher_type_id", "=", voucher_type_id.id)]
            ).mapped(lambda r: r.journal_id.id)
            document.allowed_journal_br_ids = journal_ids

    allowed_journal_br_ids = fields.Many2many(
        string="Allowed Bank Receipt Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journal_br_ids",
        store=False,
    )

    @api.multi
    def _compute_allowed_journal_cr_ids(self):
        voucher_type_id = self.env.ref(
            "account_voucher_bank_cash.voucher_type_cash_receipt"
        )
        obj_voucher_type_allowed_journal = self.env[
            "account.voucher_type_allowed_journal"
        ]

        for document in self:
            journal_ids = obj_voucher_type_allowed_journal.search(
                [("voucher_type_id", "=", voucher_type_id.id)]
            ).mapped(lambda r: r.journal_id.id)
            document.allowed_journal_cr_ids = journal_ids

    allowed_journal_cr_ids = fields.Many2many(
        string="Allowed Cash Receipt Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journal_cr_ids",
        store=False,
    )

    @api.multi
    def action_cancel(self):
        _super = super(AccountDebtCollection, self)
        result = _super.action_cancel()
        for document in self:
            for bank_detail in document.bank_detail_ids:
                if not bank_detail._check_bank_receipt_cancel():
                    msg = _("Bank Receipts must be on <Draft> state")
                    raise UserError(msg)
                bank_detail.bank_receipt_id.unlink()
            document.bank_detail_ids.unlink()

            for cash_detail in document.cash_detail_ids:
                if not cash_detail._check_cash_receipt_cancel():
                    msg = _("Cash Receipts must be on <Draft> state")
                    raise UserError(msg)
                cash_detail.cash_receipt_id.unlink()
            document.cash_detail_ids.unlink()
        return result

    @api.multi
    def _prepare_bank_receipt_data(self, document):
        self.ensure_one()

        return {
            "payment_mode_id": document.payment_mode_id.id,
        }

    @api.multi
    def _create_bank_receipt(self):
        self.ensure_one()

        voucher_type_id = self.env.ref(
            "account_voucher_bank_cash.voucher_type_bank_receipt"
        )

        obj_bank_receipt = self.env["account.bank_receipt"]
        obj_bank_receipt_line = self.env["account.bank_receipt_line"]

        if self.bank_detail_ids:
            for bank in self.bank_detail_ids:
                if bank.detail_ids:
                    voucher_data = self._prepare_receipt_voucher_data(
                        bank, voucher_type_id
                    )
                    bank_data = self._prepare_bank_receipt_data(bank)
                    bank_data.update(voucher_data)
                    br = obj_bank_receipt.create(bank_data)
                    bank.write({"bank_receipt_id": br.id})
                    for bank_detail in bank.detail_ids:
                        br_line = obj_bank_receipt_line.create(
                            self._prepare_receipt_voucher_line_data(br, bank_detail)
                        )
                        bank_detail.write({"bank_receipt_line_id": br_line.id})
        return True

    @api.multi
    def _create_cash_receipt(self):
        self.ensure_one()

        voucher_type_id = self.env.ref(
            "account_voucher_bank_cash.voucher_type_cash_receipt"
        )

        obj_cash_receipt = self.env["account.cash_receipt"]
        obj_cash_receipt_line = self.env["account.cash_receipt_line"]

        if self.cash_detail_ids:
            for cash in self.cash_detail_ids:
                if cash.detail_ids:
                    cr = obj_cash_receipt.create(
                        self._prepare_receipt_voucher_data(cash, voucher_type_id)
                    )
                    cash.write({"cash_receipt_id": cr.id})
                    for cash_detail in cash.detail_ids:
                        cr_line = obj_cash_receipt_line.create(
                            self._prepare_receipt_voucher_line_data(cr, cash_detail)
                        )
                        cash_detail.write({"cash_receipt_line_id": cr_line.id})
        return True

    @api.multi
    def _check_auto_post_bank_receipt(self):
        self.ensure_one()
        if self.collection_type_id.autopost_bank_receipt:
            for bank in self.bank_detail_ids:
                bank.bank_receipt_id.workflow_action_confirm()
                bank.bank_receipt_id.workflow_action_approve()
                bank.bank_receipt_id.workflow_action_post()

    @api.multi
    def _check_auto_post_cash_receipt(self):
        self.ensure_one()
        if self.collection_type_id.autopost_cash_receipt:
            for cash in self.cash_detail_ids:
                cash.cash_receipt_id.workflow_action_confirm()
                cash.cash_receipt_id.workflow_action_approve()
                cash.cash_receipt_id.workflow_action_post()

    @api.multi
    def action_done(self):
        _super = super(AccountDebtCollection, self)
        result = _super.action_done()
        for document in self:
            document._create_bank_receipt()
            document._check_auto_post_bank_receipt()

            document._create_cash_receipt()
            document._check_auto_post_cash_receipt()
        return result

    @api.multi
    def _get_bank_receipts(self):
        return self.mapped("bank_detail_ids.bank_receipt_id")

    @api.multi
    def _get_action_bank_receipt(self):
        action = self.env.ref(
            "account_voucher_bank_cash." "account_bank_receipt_action"
        ).read()[0]
        return action

    @api.multi
    def action_view_bank_receipts(self):
        self.ensure_one()
        receipts = self._get_bank_receipts()
        action = self._get_action_bank_receipt()

        if len(receipts) > 0:
            action["domain"] = [("id", "in", receipts.ids)]
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action

    @api.multi
    def _get_cash_receipts(self):
        return self.mapped("cash_detail_ids.cash_receipt_id")

    @api.multi
    def _get_action_cash_receipt(self):
        action = self.env.ref(
            "account_voucher_bank_cash." "account_cash_receipt_action"
        ).read()[0]
        return action

    @api.multi
    def action_view_cash_receipts(self):
        self.ensure_one()
        receipts = self._get_cash_receipts()
        action = self._get_action_cash_receipt()

        if len(receipts) > 0:
            action["domain"] = [("id", "in", receipts.ids)]
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action
