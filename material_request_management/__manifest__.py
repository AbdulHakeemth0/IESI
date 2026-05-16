# -*- coding: utf-8 -*-
{
    'name': 'Material Request Management',
    'version': '18.0.0.0',
    'summary': 'Brief description of the module',
    'description': '''
        Detailed description of the module
    ''',
    'category': 'Uncategorized',
    'depends': ['stock', 'project_management', 'base','purchase'],
    'data': [
        'data/ir_sequence.xml',
        'security/ir.model.access.csv',
        'views/project_material_request_views.xml',
        'views/project_project_views.xml',
        'reports/paperformat.xml',
        'reports/report_action.xml',
        # 'reports/report_header.xml',
        'reports/report_template.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}