from odoo import models, fields, api

class WaterSupply(models.Model):
    _name ='water.supply'
    _description = 'Water Supply'
    _rec_name = "water_name"

    water_name = fields.Char(string="Name")
    water_unit_rate = fields.Float(
        string="Unit Rate",
        digits=(16, 3)
    )