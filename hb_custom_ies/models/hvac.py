from string import digits

from odoo import models, fields, api

class HVAC(models.Model):
    _name = "hvac.item"
    _description = "HVAC"
    _rec_name = "name"

    name = fields.Char(string="Name")
    hv_unit_rate = fields.Float(
        string="Unit Rate",
        digits=(16, 3)
    )
class Sundering(models.Model):
    _name= "sundering"
    _description="Sundering"
    _rec_name = "name"

    name = fields.Char(string="Name")
    sun_unit_rate = fields.Float(string="Unit Rate", digits=(16,3))

class Measurement(models.Model):
    _name = "measurement"
    _description = "Measurement"
    _rec_name = "measu_name"

    measu_name = fields.Char(string="Measurement Name")
