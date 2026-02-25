from odoo import models, fields, api
from datetime import datetime, timedelta, date


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    emp_sequence = fields.Char(string='Employee Seequence', copy=False, readonly=True, index=True, group_operator=False)
    visa_reminder_sent = fields.Boolean(string="Visa Reminder Sent", default=False)

    @api.model
    def create(self, vals):
        if not vals.get('emp_sequence'):
            vals['emp_sequence'] = self.env['ir.sequence'].next_by_code('hr.employee.emp_sequence') or '/'
        return super().create(vals)

    def action_assign_missing_emp_codes(self):
        sequence = self.env['ir.sequence']
        for emp in self.search([('emp_sequence', '=', False)]):
            emp.emp_sequence = sequence.next_by_code('hr.employee.emp_sequence')

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = args[:]
        if name:
            domain = ['|', '|',
                      ('emp_sequence', 'ilike', name),
                      ('name', 'ilike', name),
                      ('work_email', 'ilike', name)] + domain
        employees = self.search(domain, limit=limit)
        return employees.name_get()

    def name_get(self):
        result = []
        for rec in self:
            display_name = f"{rec.emp_sequence or ''} - {rec.name or ''}"
            result.append((rec.id, display_name))
        return result

    work_type = fields.Selection(
        [
            ('office', 'Office'),
            ('site', 'Site'),
        ],
        string='Work Location',
        required=True,
        default='site'
    )


    employee_type_id = fields.Many2one('hr.contract.type', string='Employee Type')


