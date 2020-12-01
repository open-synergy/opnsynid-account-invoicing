# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models


class SignatureDefinition(models.Model):
    _inherit = "signature.definition"

    @api.model
    def _get_signature_validation_model_names(self):
        res = \
            super(
                SignatureDefinition, self
            )._get_signature_validation_model_names()
        res.append("account.invoice")
        return res
