# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountDebtCollectionType(models.Model):
    _name = "account.debt_collection_type"
    _description = "Debt Collection Type"

    name = fields.Char(
        string="Collection Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    days_before_due = fields.Integer(
        string="Days Before Due",
        required=True,
        default=0,
    )
    days_after_due = fields.Integer(
        string="Days After Due",
        required=True,
        default=0,
    )
    allowed_collector_ids = fields.Many2many(
        string="Allowed Collectors",
        comodel_name="res.users",
        relation="rel_collection_type_allowed_collector",
        column1="collection_type_id",
        column2="user_id",
    )
    allowed_journal_ids = fields.Many2many(
        string="Allowed Journals",
        comodel_name="account.journal",
        relation="rel_collection_type_allowed_journal",
        column1="collection_type_id",
        column2="journal_id",
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    collection_confirm_group_ids = fields.Many2many(
        string="Allow To Confirm",
        comodel_name="res.groups",
        relation="rel_collection_type_allowed_confirm",
        column1="collection_type_id",
        column2="group_id",
    )
    collection_open_group_ids = fields.Many2many(
        string="Allow To Approve",
        comodel_name="res.groups",
        relation="rel_collection_type_allowed_open",
        column1="collection_type_id",
        column2="group_id",
    )
    collection_done_group_ids = fields.Many2many(
        string="Allow To Finish",
        comodel_name="res.groups",
        relation="rel_collection_type_allowed_done",
        column1="collection_type_id",
        column2="group_id",
    )
    collection_cancel_group_ids = fields.Many2many(
        string="Allow To Cancel",
        comodel_name="res.groups",
        relation="rel_collection_type_allowed_cancel",
        column1="collection_type_id",
        column2="group_id",
    )
    collection_restart_group_ids = fields.Many2many(
        string="Allow To Restart",
        comodel_name="res.groups",
        relation="rel_collection_type_allowed_restart",
        column1="collection_type_id",
        column2="group_id",
    )
    collection_print_group_ids = fields.Many2many(
        string="Allow To Print",
        comodel_name="res.groups",
        relation="rel_collection_type_allowed_print",
        column1="collection_type_id",
        column2="group_id",
    )
