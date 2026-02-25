# __manifest__.py
{
    'name': 'Bi Time Approval',
    'version': '18.0.1.0.4',
    'category': 'Human Resources',
    'summary': 'Approval for attendance by Team Leader and HR',
    'author': 'Abdul Hakeem TH',
    'company': 'Hornbill Business Spc',
    'maintainer': 'Hornbill Business Spc',
    'website': 'https://hornbill-bs.com',
    'category': 'hr',
    'depends': ["base",'hr','hr_holidays','hr_attendance','mail'],
    'data': [
        "data/activity.xml",
        "data/data.xml",
        "views/hr_attendance_views.xml",
        "views/hr_job.xml",
        'views/hr_leave.xml',
        
        

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3', 
}
