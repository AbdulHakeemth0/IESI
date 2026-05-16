from odoo import models, fields, api

class DrainageItem(models.Model):
    _name = "drainage.item"
    _description = "Drainage Item"
    _rec_name = "drainage_item_name"

    drainage_item_name = fields.Char(string="Name")
    drainage_unit_rate = fields.Float(
        string="Unit Rate",
        digits="Product Unit of Measure",
    )