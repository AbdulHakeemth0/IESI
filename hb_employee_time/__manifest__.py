# __manifest__.py
{
    'name': 'Hb Employee Time ',
    'version': '18.0.1.0.4',
    'category': 'Human Resources',
    'summary': 'Approval for attendance by Team Leader and HR',
    'author': 'Abdul Hakeem TH',
    'company': 'Hornbill Business Spc',
    'maintainer': 'Hornbill Business Spc',
    'website': 'https://hornbill-bs.com',
    'category': 'hr',
    'depends': ["base", 'hr', 'hr_holidays', 'hr_attendance','mail','hr_payroll','accountant'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/inherit_employee.xml',
        'views/inherit_res_company.xml',
        'views/inherit_res_partner.xml',
        'views/mode_payment.xml',
        'data/employee_number_sequence.xml',
        'data/ir_cron_data.xml',
        'data/data.xml',
        # 'views/activity.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}