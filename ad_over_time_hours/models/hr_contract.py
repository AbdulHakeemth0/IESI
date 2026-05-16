from odoo import fields, models


class AdHrContract(models.Model):

    _inherit = 'hr.contract'

    daily_working_hours = fields.Float(string="Standard Working Hours", default=10.0, tracking=True)
    daily_wage = fields.Monetary(string="Daily Wage",  default=10.0,tracking=True)
