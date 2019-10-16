# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class AccountDebtCollectionVoucherDetailCommon(models.AbstractModel):
    _name = "account.debt_collection_voucher_detail_common"
    _description = "Abstract Model for Debt Collection Detail Voucher"

    collection_voucher_id = fields.Many2one(
        string="# Collection Bank",
        comodel_name="account.debt_collection_voucher_common",
        required=True,
        ondelete="cascade",
    )
    collection_detail_id = fields.Many2one(
        string="# Collection Detail",
        comodel_name="account.debt_collection_detail",
        ondelete="cascade",
        required=True,
    )
    amount = fields.Float(
        string="Amount",
        default=1.0,
    )

    @api.multi
    @api.onchange(
        "collection_detail_id",
    )
    def onchange_amount(self):
        if self.collection_detail_id:
            self.amount =\
                self.collection_detail_id.invoice_id.residual

    @api.constrains(
        "collection_voucher_id",
        "collection_detail_id"
    )
    def _check_collection_detail_id(self):
        if self.collection_detail_id:
            strWarning = _("No duplicate collection")
            collection_voucher_id =\
                self.collection_voucher_id
            collection_detail_id =\
                self.collection_detail_id.id
            check_collection =\
                self.search([
                    ("collection_voucher_id", "=", collection_voucher_id.id),
                    ("collection_detail_id", "=", collection_detail_id.id)
                ])
            if len(check_collection) > 1:
                raise UserError(strWarning)
