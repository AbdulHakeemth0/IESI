from odoo import models, fields, api

class FireFightingItem(models.Model):
    _name = "fire.fighting.item"
    _description = "Fire Fighting Item"
    _rec_name = "fire_fighting_item_name"

    fire_fighting_item_name = fields.Char(string="Name")
    fire_fighting_unit_rate = fields.Float(
        string="Unit Rate",
        digits="Product Unit of Measure",
    )