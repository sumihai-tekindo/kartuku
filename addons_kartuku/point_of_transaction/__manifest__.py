# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Point of Transaction',
    'category': 'Tools',
    'summary': 'PoT',
    'description': """
""",
    'depends': ['base','stock','sale','sales_team'],
    'data': [
        'views/point_of_transaction_view.xml',
        'views/analysis_report_view.xml',
    ],
    'application': True,
}
