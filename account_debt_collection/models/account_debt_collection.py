# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountDebtCollection(models.Model):
    _name = "account.debt_collection"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _description = "Debt Collection"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    @api.model
    def _default_date(self):
        return fields.Datetime.now()

    @api.multi
    def _compute_policy(self):
        _super = super(AccountDebtCollection, self)
        _super._compute_policy()

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        default=lambda self: self._default_user_id(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        default=lambda self: self._default_date(),
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    collection_type_id = fields.Many2one(
        string="Type",
        comodel_name="account.debt_collection_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    collector_id = fields.Many2one(
        string="Collector",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="account.debt_collection_detail",
        inverse_name="debt_collection_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
    )

    detail_summary_ids = fields.One2many(
        string="Detail Summary By Partner",
        comodel_name="account.debt_collection_detail_summary",
        inverse_name="debt_collection_id",
        readonly=True,
    )

    @api.multi
    @api.depends(
        "detail_ids",
        "detail_ids.amount_due",
        "detail_ids.amount_collected",
    )
    def _compute_total_amount(self):
        for document in self:
            total_amount_due = 0.0
            total_amount_collected = 0.0
            for line in document.detail_ids:
                total_amount_due += line.amount_due
                total_amount_collected += line.amount_collected
            document.total_amount_due = total_amount_due
            document.total_amount_collected = total_amount_collected

    total_amount_due = fields.Float(
        string="Total Amount Due",
        compute="_compute_total_amount",
        store=True,
    )

    total_amount_collected = fields.Float(
        string="Total Collected Amount",
        compute="_compute_total_amount",
        store=True,
    )

    @api.multi
    @api.depends(
        "total_amount_due",
        "total_amount_collected",
    )
    def _compute_collection_rate(self):
        for document in self:
            total_amount_due = document.total_amount_due
            total_amount_collected = document.total_amount_collected
            try:
                document.collection_rate = total_amount_collected / total_amount_due
            except ZeroDivisionError:
                document.collection_rate = 0

    collection_rate = fields.Float(
        string="Collection Rate (Dec)",
        compute="_compute_collection_rate",
        store=True,
    )

    @api.multi
    def _compute_allowed_invoice_ids(self):
        obj_account_invoice = self.env["account.invoice"]

        for document in self:
            invoice_ids = obj_account_invoice.search(
                document._prepare_general_criteria_invoice()
            )
            document.allowed_invoice_ids = invoice_ids.ids

    allowed_invoice_ids = fields.Many2many(
        string="Allowed Invoices",
        comodel_name="account.invoice",
        compute="_compute_allowed_invoice_ids",
        store=False,
    )

    @api.multi
    def _compute_allowed_invoice_specific_ids(self):
        obj_account_invoice = self.env["account.invoice"]

        for document in self:
            invoice_ids = obj_account_invoice.search(
                document._prepare_criteria_specific_invoice()
            )
            document.allowed_invoice_specific_ids = invoice_ids.ids

    allowed_invoice_specific_ids = fields.Many2many(
        string="Allowed Specific Invoices",
        comodel_name="account.invoice",
        compute="_compute_allowed_invoice_specific_ids",
        store=False,
    )

    @api.multi
    @api.depends("collection_type_id")
    def _compute_allowed_collector_ids(self):
        obj_debt_collection_type = self.env["account.debt_collection_type"]

        for document in self:
            collection_type_id = obj_debt_collection_type.search(
                [("id", "=", document.collection_type_id.id)]
            )
            document.allowed_collector_ids = (
                collection_type_id.allowed_collector_ids.ids
            )

    allowed_collector_ids = fields.Many2many(
        string="Allowed Collectors",
        comodel_name="res.users",
        compute="_compute_allowed_collector_ids",
        store=False,
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "On Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )
    # Policy Field
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    open_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
    )
    done_ok = fields.Boolean(
        string="Can Finish",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    print_ok = fields.Boolean(
        string="Can Print",
        compute="_compute_policy",
    )
    # Log Fields
    confirm_date = fields.Datetime(
        string="Confirm Date",
        readonly=True,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
    )
    open_user_id = fields.Many2one(
        string="Approve By",
        comodel_name="res.users",
        readonly=True,
    )
    open_date = fields.Datetime(
        string="Approve Date",
        readonly=True,
    )
    done_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
    )
    done_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
    )

    @api.multi
    @api.onchange(
        "collection_type_id",
    )
    def onchange_collector_id(self):
        if self.collection_type_id:
            self.collector_id = False

    @api.multi
    def _prepare_general_criteria_invoice(self):
        self.ensure_one()
        result = [("id", "=", 0)]
        allowed_journal_ids = self.collection_type_id.allowed_journal_ids.ids

        if allowed_journal_ids:
            result = [
                ("state", "=", "open"),
                ("type", "=", "out_invoice"),
                ("journal_id", "in", allowed_journal_ids),
            ]
        return result

    @api.multi
    def _prepare_criteria_specific_invoice(self):
        self.ensure_one()
        criteria = self._prepare_general_criteria_invoice()
        collector_id = self.collector_id.id
        criteria += [
            ("partner_id.collector_id", "=", collector_id),
        ]
        if self.date:
            date = datetime.strptime(self.date, "%Y-%m-%d")
            days_after_due = self.collection_type_id.days_after_due
            days_before_due = self.collection_type_id.days_before_due

            date_after_invoice_due = self._get_date_after_invoice_due(
                date, days_after_due
            ).strftime("%Y-%m-%d")
            date_before_invoice_due = self._get_date_before_invoice_due(
                date, days_before_due
            ).strftime("%Y-%m-%d")
            result = [
                ("date_due", ">=", date_before_invoice_due),
                ("date_due", "<=", date_after_invoice_due),
            ]
            result += criteria
        else:
            result = criteria
        return result

    @api.model
    def _get_date_before_invoice_due(self, date, days_before_due):
        result = (date - timedelta(days=days_before_due)).date()
        return result

    @api.model
    def _get_date_after_invoice_due(self, date, days_after_due):
        result = (date + timedelta(days=days_after_due)).date()
        return result

    @api.multi
    def _check_detail_ids(self):
        self.ensure_one()
        result = True
        if not len(self.detail_ids.ids):
            result = False
        return result

    @api.multi
    def _check_amount_collected(self):
        self.ensure_one()
        result = True
        for detail in self.detail_ids:
            if detail.amount_collected > detail.amount_due:
                result = False
        return result

    @api.multi
    def action_confirm(self):
        msg = _("You cannot confirm an A/R collection which has no invoice")
        for document in self:
            if not document._check_detail_ids():
                raise UserError(msg)
            document.write(document._prepare_confirm_data())

    @api.multi
    def action_start(self):
        for document in self:
            document.write(document._prepare_start_data())

    @api.multi
    def action_done(self):
        msg = _("Collected Amount Exceeded Amount Due")
        for document in self:
            if not document._check_amount_collected():
                raise UserError(msg)
            document.write(document._prepare_done_data())

    @api.multi
    def action_cancel(self):
        for document in self:
            document.detail_ids.unlink()
            document.write(document._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_start_data(self):
        self.ensure_one()
        return {
            "state": "open",
            "open_date": fields.Datetime.now(),
            "open_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        return {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "open_date": False,
            "open_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }

    @api.model
    def create(self, values):
        _super = super(AccountDebtCollection, self)
        result = _super.create(values)
        sequence = result._create_sequence()
        result.write(
            {
                "name": sequence,
            }
        )
        return result

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(AccountDebtCollection, self)
        _super.unlink()
