# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools
from psycopg2.extensions import AsIs


class AccountInvoiceLineSummary(models.Model):
    _name = "account.invoice_line_summary"
    _description = "Invoice Line Summary"
    _auto = False

    name = fields.Char(
        string="Description",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    product_qty = fields.Float(
        string="Product Qty",
    )
    product_uom_id = fields.Many2one(
        string="Product UoM",
        comodel_name="product.uom",
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.invoice",
    )
    price_unit = fields.Float(
        string="Unit Price",
    )
    discount = fields.Float(
        string="Discount",
    )
    product_qty = fields.Float(
        string="Product Qty",
    )
    price_subtotal = fields.Float(
        string="Subtotal",
    )

    def _select(self):
        select_str = """
            SELECT
                row_number() OVER() AS id,
                a.invoice_id AS invoice_id,
                a.product_id AS product_id,
                a.uos_id AS product_uom_id,
                a.name AS name,
                a.price_unit AS price_unit,
                a.discount AS discount,
                b.tax_arr AS taxes,
                SUM(a.quantity) AS product_qty,
                SUM(a.price_subtotal) AS price_subtotal
        """
        return select_str

    def _from(self):
        from_str = """
            account_invoice_line AS a
            LEFT JOIN (
                SELECT invoice_line_id,
                        array_agg(tax_id) AS tax_arr
                FROM    (
                    SELECT  invoice_line_id,
                            tax_id
                    FROM    account_invoice_line_tax
                    ORDER BY    invoice_line_id,
                                tax_id
                    ) sub
                GROUP BY 1
                ) AS b ON a.id = b.invoice_line_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY a.invoice_id,
                        a.product_id,
                        a.name,
                        a.uos_id,
                        a.price_unit,
                        a.discount,
                        b.tax_arr
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        view_query = """%s
            FROM %s
            %s""" % (
            self._select(),
            self._from(),
            self._group_by(),
        )
        cr.execute(
            "CREATE OR REPLACE VIEW %s AS %s", (AsIs(self._table), AsIs(view_query))
        )
