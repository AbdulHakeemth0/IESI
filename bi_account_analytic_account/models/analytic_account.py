from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    is_trading = fields.Boolean(string="Is Trading")
    is_project = fields.Boolean(string="Is Project")
    is_maintenance = fields.Boolean(string="Is Maintenance")


        




