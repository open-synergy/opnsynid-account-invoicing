# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools
import openerp.addons.decimal_precision as dp


class AccountDebtCollectionSummaryByDate(models.Model):
    _name = "account.debt_collection_summary_by_date"
    _description = "A/R Collection Summary By Date"
    _auto = False

    name = fields.Char(
        string="Name",
    )
    date = fields.Date(
        string="Date",
    )
    debt_collection_group = fields.Char(
        string="A/R Collection(s)",
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
            'A/R Collection Summary:'
            ||
            ' '
            ||
            to_char(b.date, 'dd/mm/yyyy') AS name,
            b.date AS date,
            SUM(a.amount_collected) AS total_amount_collected,
            string_agg(DISTINCT b.name, ', ') AS debt_collection_group,
            string_agg(c.number, ', ') AS invoice_group
        """
        return select_str

    def _from(self):
        from_str = """
            account_debt_collection_detail as a
        """
        return from_str

    def _join(self):
        join_str = """
            JOIN
                account_debt_collection as b ON a.debt_collection_id=b.id
            JOIN
                account_invoice as c ON a.invoice_id=c.id
        """
        return join_str

    def _where(self):
        where_str = """
            b.state='done'
        """
        return where_str

    def _group_by(self):
        group_by_str = """
            b.date
        """
        return group_by_str

    def _order_by(self):
        order_by_str = """
            b.date
        """
        return order_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT
                %s
            FROM
                %s
            %s
            WHERE
                %s
            GROUP BY
                %s
            ORDER BY
                %s
            )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where(),
            self._group_by(),
            self._order_by()))
