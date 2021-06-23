# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time

from openerp.tests.common import TransactionCase


class TestLineSummary(TransactionCase):
    def setUp(self):
        super(TestLineSummary, self).setUp()
        # Object
        self.obj_invoice = self.env["account.invoice"]
        self.obj_invoice_line = self.env["account.invoice.line"]

        # Data
        self.partner_1 = self.env.ref("base.res_partner_1")
        self.account = self.env.ref("account.a_recv")
        self.product_1 = self.env.ref("product.product_product_3")
        self.curr = self.env.ref("base.IDR")

    def _create_invoice(self):
        invoice_id = self.obj_invoice.create(
            {
                "partner_id": self.partner_1.id,
                "reference_type": "none",
                "currency_id": self.curr.id,
                "name": "invoice to client",
                "account_id": self.account.id,
                "type": "out_invoice",
                "date_invoice": time.strftime("%Y") + "-07-01",
            }
        )
        self.obj_invoice_line.create(
            {
                "product_id": self.product_1.id,
                "quantity": 1,
                "price_unit": 1000000,
                "invoice_id": invoice_id.id,
                "name": "Test",
            }
        )
        self.obj_invoice_line.create(
            {
                "product_id": self.product_1.id,
                "quantity": 5,
                "price_unit": 1000000,
                "invoice_id": invoice_id.id,
                "name": "Test",
            }
        )
        return invoice_id

    def test_line_summary(self, parent_menu_id=False):
        data_invoice = self._create_invoice()

        # Check Line Summary Ids Is Not None
        self.assertIsNotNone(data_invoice.line_summary_ids)

        # Check Line Summary Is Grouped By Product
        self.assertEquals(1, len(data_invoice.line_summary_ids.ids))

        # Check Line Summary Data
        self.assertEquals(6, data_invoice.line_summary_ids[0].product_qty)
        self.assertEquals(6000000, data_invoice.line_summary_ids[0].price_subtotal)
