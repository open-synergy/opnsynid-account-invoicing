# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountDebtCollection(models.Model):
    _inherit = "account.debt_collection"

    @api.multi
    def _compute_allowed_partner_ids(self):
        obj_collection_detail = self.env["account.debt_collection_detail"]

        for document in self:
            if isinstance(document.id, models.NewId):
                continue
            partner_ids = obj_collection_detail.search(
                [("debt_collection_id", "=", document.id)]
            ).mapped(lambda r: r.invoice_id.partner_id.id)
            document.allowed_partner_ids = partner_ids

    allowed_partner_ids = fields.Many2many(
        string="Allowed Partners",
        comodel_name="res.partner",
        compute="_compute_allowed_partner_ids",
        store=False,
    )

    @api.multi
    def _prepare_criteria_move_line(self, voucher, collection_detail):
        self.ensure_one()

        commercial_partner_id = voucher.partner_id.commercial_partner_id.id
        move_id = collection_detail.invoice_id.move_id.id

        criteria = [
            ("move_id", "=", move_id),
            ("account_id.reconcile", "=", True),
            ("reconcile_id", "=", False),
            ("partner_id", "=", commercial_partner_id),
            ("debit", ">", 0),
        ]

        return criteria

    @api.multi
    def _prepare_receipt_voucher_data(self, document, voucher_type_id):
        self.ensure_one()

        journal = document.journal_id
        account_id = (
            journal.default_debit_account_id
            and journal.default_debit_account_id.id
            or False
        )
        write_off_account = document._get_write_off_account()
        description = "Payment from %s" % (self.name)
        reference = ""
        if document.reference != "/":
            reference = "References: %s" % (document.reference)

        return {
            "description": description,
            "account_id": account_id,
            "voucher_date": document.date,
            "period_id": document.period_id.id,
            "type_id": voucher_type_id.id,
            "journal_id": journal.id,
            "partner_id": document.partner_id.id,
            "amount": document.amount_real,
            "note": reference,
            "writeoff_account_id": write_off_account and write_off_account.id or False,
        }

    @api.multi
    def _prepare_receipt_voucher_line_data(self, voucher, document):
        self.ensure_one()

        obj_account_move_line = self.env["account.move.line"]

        collection_detail = document.collection_detail_id

        criteria_move_line = self._prepare_criteria_move_line(
            voucher, collection_detail
        )

        move_line_id = obj_account_move_line.search(criteria_move_line)

        return {
            "name": move_line_id.name,
            "voucher_id": voucher.id,
            "partner_id": voucher.partner_id.id,
            "move_line_id": move_line_id.id,
            "account_id": collection_detail.invoice_id.account_id.id,
            "amount": document.amount,
            "type": "cr",
        }
