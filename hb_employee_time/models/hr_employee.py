from odoo import models, fields, api
from datetime import datetime, timedelta, date


class HrEmployeeRemainder(models.Model):
    _name = 'hr.employee.remainder'
    _description = 'Employee Remainder'



    def send_visa_expire_alert_remainder(self):

        for employee in self.env['hr.employee'].search([('visa_expire', '!=', False)]):
            if (employee.visa_expire - fields.Date.today()).days <= 7:
                mail_values = {
                    'email_to': 'admin@iesioman.com',
                    'subject': "Employee Visa Expire Remainder for %s" % employee.name,
                    # 'recipient_ids': [(6,0, [66])],
                    'body_html': "Reminder Email: Employee %s  has upcoming visa expire on %s" % (employee.name, fields.Date. today()),
                }
                print('mail_values', mail_values)
                mail  = self.env['mail.mail'].sudo().create(mail_values)
                mail.send()
                print('mail',mail)

