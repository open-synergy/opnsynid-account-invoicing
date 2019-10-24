# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools
import openerp.addons.decimal_precision as dp


class AccountDebtCollectionDetailSummary(models.Model):
    _name = "account.debt_collection_detail_summary"
    _description = "Debt Collection Detail Summary"
    _auto = False

    debt_collection_id = fields.Many2one(
        string="# Collection",
        comodel_name="account.debt_collection",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    invoice_group = fields.Char(
        string="Invoice(s)",
    )
    total_amount_collected = fields.Float(
        string="Total Collected Amount",
        digits=dp.get_precision("Account"),
    )

    def _select(self):
        select_str = """
            row_number() OVER() AS id,
            a.debt_collection_id AS debt_collection_id,
            b.partner_id AS partner_id,
            SUM(a.amount_collected) AS total_amount_collected,
            string_agg(b.number, ', ') AS invoice_group
        """
        return select_str

    def _from(self):
        from_str = """
            account_debt_collection_detail as a
        """
        return from_str

    def _join(self):
        join_str = """
            account_invoice as b on a.invoice_id=b.id
        """
        return join_str

    def _group_by(self):
        group_by_str = """
            a.debt_collection_id, b.partner_id
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT
                %s
            FROM
                %s
            JOIN
                %s
            GROUP BY
                %s
            )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._group_by()))
