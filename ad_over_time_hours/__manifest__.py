# -*- coding: utf-8 -*-
{
    'name': 'Overtime Pay management',
    'version': '18.0.0.0',
    'summary': 'Overtime Pay Management',
    'description': '''
        Overtime Pay Management'
    ''',
    'category': 'HR',
    'depends': ['hr_payroll','sale_timesheet'],
    'data': [
        'views/hr_contract.xml',
        'views/hr_timesheet.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
