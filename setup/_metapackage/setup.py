import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-open-synergy-opnsynid-account-invoicing",
    description="Meta package for open-synergy-opnsynid-account-invoicing Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-account_invoice_day_overdue',
        'odoo11-addon-account_invoice_ematerai',
        'odoo11-addon-account_invoice_full_description_to_journal_item',
        'odoo11-addon-account_invoice_last_payment',
        'odoo11-addon-account_invoice_multiple_approval',
        'odoo11-addon-account_invoice_proforma',
        'odoo11-addon-account_invoice_reversal',
        'odoo11-addon-account_invoice_reversal_deferred_revenue',
        'odoo11-addon-account_invoice_reversal_deferred_revenue_extra_move',
        'odoo11-addon-account_invoice_source_document',
        'odoo11-addon-account_invoice_workflow_policy',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 11.0',
    ]
)
