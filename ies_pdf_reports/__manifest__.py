# -*- coding: utf-8 -*-
{
    'name': 'Custome pdf report',
    'version': '18.0.0.0',
    'summary': 'Custome pdf report',
    'description': '''
        Custome pdf report
    ''',
    'category': 'Uncategorized',
    'depends': ['purchase','account','sale_management',  'pdf_report_with_watermark','stock'],
    'data': [
        'data/product_sequence.xml',
        'report/iesi_po_template.xml',
        'report/reports.xml',
        'report/iesi_invoice_template.xml',
        'report/ies_quotation_template.xml',
        'views/account_move_view.xml',
        'views/purchase_order.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}