# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Account Invoice E-Materai",
    "version": "11.0.1.0.0",
    "license": "LGPL-3",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "account",
        "ssi_ematerai_mixin",
    ],
    "data": [
        "data/ematerai_parameter_data.xml",
    ],
    "installable": True,
    "auto_install": False,
}
