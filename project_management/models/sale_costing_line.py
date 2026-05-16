# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api, fields, models


class SaleCostingLine(models.Model):
    """ This model represents sale.costing.line."""
    _inherit = 'sale.costing.line'

    template_line_id = fields.Many2one('project.material.template.line')