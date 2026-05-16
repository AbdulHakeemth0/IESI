from odoo import models, fields, api

class MEP(models.Model):
    _name = "mep.item"
    _description = "MEP"
    _rec_name = "mep_name"

    mep_name = fields.Char(string="Name")
    mep_unit_rate = fields.Float(
        string="Unit Rate",
        digits=(16, 3)
    )