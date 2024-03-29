# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openerp.addons.decimal_precision as dp
from openerp import fields, models, tools
from psycopg2.extensions import AsIs


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
        view_query = """
            SELECT
                {}
            FROM
                {}
            JOIN
                {}
            GROUP BY
                {}
            """.format(
            self._select(),
            self._from(),
            self._join(),
            self._group_by(),
        )
        cr.execute(
            "CREATE OR REPLACE VIEW %s AS %s", (AsIs(self._table), AsIs(view_query))
        )
