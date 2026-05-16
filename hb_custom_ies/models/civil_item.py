from odoo import models, fields, api

class CivilItem(models.Model):
    _name = "civil.item"
    _description = "Civil Item"
    _rec_name = "civil_item_name"

    civil_item_name = fields.Char(string="Name")
    civil_unit_rate = fields.Float(
        string="Unit Rate",
        digits="Product Unit of Measure",
    )