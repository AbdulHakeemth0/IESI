# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    mr_id = fields.Many2one('project.material.request', string="MR")
