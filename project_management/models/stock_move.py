# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    project_material_id = fields.Many2one('project.material.line')
