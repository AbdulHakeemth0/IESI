# -*- coding: utf-8 -*-
{
    'name': 'Project Management',
    'version': '18.0.0.0',
    'summary': 'Project Management',
    'description': '''
        Project Management
    ''',
    'category': 'Uncategorized',
    'depends': ['base', 'project', 'sale_project', 'hb_custom_ies', 'timesheet_grid', 'stock_dropshipping'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
        'views/project_material_template.xml',
        'views/inherit_sale_order.xml',
        'wizards/rfq_creation_wizard.xml',
        'wizards/material_request_wizard.xml',
		'views/project_event.xml',
		'views/stock_picking.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}