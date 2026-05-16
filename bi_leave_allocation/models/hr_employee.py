from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    joining_date = fields.Date(string="Joining Date",tracking=True)
    is_early_leave_app = fields.Boolean(string="Early Annual Leave Applicable")
    is_annual_ticket = fields.Boolean(string="Annual Ticket")
    family_visa_applicable = fields.Boolean(string='Family Visa Applicable')
    vehicle_applicable = fields.Boolean(string='Vehicle Allowed')


   