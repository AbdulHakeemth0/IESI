from odoo import models, fields, api

class ELVItem(models.Model):
    _name = "elv.item"
    _description = "ELV Item"
    _rec_name = "elv_item_name"

    elv_item_name = fields.Char(string="Name")
    elv_unit_rate = fields.Float(
        string="Unit Rate",
        digits="Product Unit of Measure",
    )