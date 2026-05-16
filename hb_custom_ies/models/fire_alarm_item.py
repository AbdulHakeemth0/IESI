from odoo import models, fields, api

class FireAlarmItem(models.Model):
    _name = "fire.alarm.item"
    _description = "Fire Alarm Item"
    _rec_name = "fire_alarm_item_name"

    fire_alarm_item_name = fields.Char(string="Name")
    fire_alarm_unit_rate = fields.Float(
        string="Unit Rate",
        digits="Product Unit of Measure",
    )