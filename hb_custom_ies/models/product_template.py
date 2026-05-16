# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    is_costing_charge = fields.Boolean("Is costing charge")