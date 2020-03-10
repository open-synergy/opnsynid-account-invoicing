# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountDebtCollectionSchedule(models.Model):
    _name = "account.debt_collection_schedule"
    _description = "Account Debt Collection Schedule"

    name = fields.Char(
        string="Description",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Code",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="account.debt_collection_type",
        required=True,
    )

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_allowed_collector_ids(self):
        obj_collection_type =\
            self.env["account.debt_collection_type"]

        for document in self:
            if document.type_id:
                collection_type_ids =\
                    obj_collection_type.search([
                        ("id", "=", document.type_id.id)
                    ])
                document.allowed_collector_ids =\
                    collection_type_ids.allowed_collector_ids

    allowed_collector_ids = fields.Many2many(
        string="Allowed Collectors",
        comodel_name="res.users",
        compute="_compute_allowed_collector_ids",
        store=False,
    )
    collector_id = fields.Many2one(
        string="Collector",
        comodel_name="res.users",
        required=True,
    )

    @api.multi
    @api.depends(
        "collector_id",
    )
    def _compute_allowed_partner_ids(self):
        obj_res_partner =\
            self.env["res.partner"]

        for document in self:
            if document.collector_id:
                partner_ids =\
                    obj_res_partner.search([
                        ("collector_id", "=", document.collector_id.id)
                    ])
                document.allowed_partner_ids = partner_ids.ids

    allowed_partner_ids = fields.Many2many(
        string="Allowed Partners",
        comodel_name="res.partner",
        compute="_compute_allowed_partner_ids",
        store=False,
    )
    partner_ids = fields.Many2many(
        string="Partner(s)",
        comodel_name="res.partner",
        relation="rel_collection_schedule_2_partner",
        column1="collection_schedule_id",
        column2="partner_id",
    )
    cron_id = fields.Many2one(
        string="Cron",
        comodel_name="ir.cron",
        readonly=True,
    )

    @api.multi
    @api.onchange(
        "type_id",
    )
    def onchange_collector_id(self):
        if self.type_id:
            self.collector_id = False

    @api.multi
    @api.onchange(
        "collector_id",
    )
    def onchange_partner_ids(self):
        if self.collector_id:
            self.partner_ids = False

    @api.multi
    def action_create_cron(self):
        for document in self:
            document._generate_cron()

    @api.multi
    def action_delete_cron(self):
        for document in self:
            document.cron_id.unlink()

    @api.multi
    def _generate_cron(self):
        self.ensure_one()
        data = self._prepare_cron_data()
        obj_cron = self.env["ir.cron"]
        cron = obj_cron.create(data)
        self.write({"cron_id": cron.id})

    @api.multi
    def _prepare_cron_data(self):
        self.ensure_one()
        cron_name = "Account Debt Collection Schedule: %s" % (
            self.name)
        return {
            "name": cron_name,
            "user_id": self.env.user.id,
            "active": True,
            "interval_number": 1,
            "interval_type": "days",
            "numberofcall": -1,
            "doall": True,
            "model": "account.debt_collection_schedule",
            "function": "cron_create_debt_collection",
            "args": "(%s,)" % (self.id),
        }

    @api.model
    def cron_create_debt_collection(self, collection_schedule_id):
        collection_schedule =\
            self.browse([collection_schedule_id])[0]
        collection_schedule._create_collection()

    @api.multi
    def _prepare_collection_data(self):
        self.ensure_one()
        return {
            "collection_type_id": self.type_id.id,
            "collector_id": self.collector_id.id,
            "cron_create_date": fields.Datetime.now(),
            "cron_create_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_collection_detail_data(
        self,
        collection,
        invoice,
    ):
        self.ensure_one()
        return {
            "debt_collection_id": collection.id,
            "invoice_id": invoice.id,
        }

    @api.multi
    def _create_collection(self):
        self.ensure_one()
        obj_account_debt_collection =\
            self.env["account.debt_collection"]
        obj_account_debt_collection_detail =\
            self.env["account.debt_collection_detail"]
        obj_account_invoice =\
            self.env["account.invoice"]
        collection = obj_account_debt_collection.create(
            self._prepare_collection_data())
        criteria_invoice =\
            collection._prepare_criteria_specific_invoice()
        invoice_ids =\
            obj_account_invoice.search(
                criteria_invoice
            ).filtered(lambda r: r.partner_id.id in self.partner_ids.ids)
        if invoice_ids:
            for invoice in invoice_ids:
                obj_account_debt_collection_detail.create(
                    self._prepare_collection_detail_data(
                        collection, invoice))
