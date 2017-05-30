# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Contacts Kartuku',
    'category': 'Tools',
    'summary': 'Customers, Vendors, Partners,...',
    'description': """
""",
    'depends': ['base','sale','sales_team'],
    'data': [
        'views/data_partner_type.xml',
        'views/contact_kartuku_view.xml',
        'views/partner_type_view.xml',
    ],
    'application': True,
}
