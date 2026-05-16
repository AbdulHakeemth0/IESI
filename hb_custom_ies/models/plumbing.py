from odoo import models, fields, api

class Plumbing(models.Model):
    _name ='plumbing'
    _description = 'Plumbing'
    _rec_names = "plumbing_name"

    plumbing_name = fields.Char(string="Name")
    plumbing_unit_rate = fields.Float(
        string="Unit Rate",
        digits=(16, 3)
    )