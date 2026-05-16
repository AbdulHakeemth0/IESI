{
    'name': 'Partner Code Automatic Generation in Odoo 18',
    'summary': 'Auto-generate and display partner codes',
    'version': '18.0.0.0.1',
    'category': 'Contacts',
    'author': 'Abdul Hakeem TH',
    'website': 'https://hornbill-bs.com',
    'depends': ['base'],
    'data': [
        'data/partner_sequence.xml',
        'data/server_action.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    "license": 'LGPL-3',
}