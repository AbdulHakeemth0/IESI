from odoo import models, fields, api

class ElectricalItem(models.Model):
    _name = "electrical.item"
    _description = "Electrical Item"
    _rec_names = "name"


    name = fields.Char(string="Item Name", required=True)
    unit_rate = fields.Float(
        string="Unit Rate",
        digits=(16, 3)
    )

