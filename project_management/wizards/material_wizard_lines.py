# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

class MaterialWizardLines(models.TransientModel):
    _name = "material.wizard.lines"
    _description = "Material Wizard Lines"

    wizard_id = fields.Many2one('material.request.wizard')
    product_id = fields.Many2one('product.product')
    quantity = fields.Float(string="Quantity to purchase", digits='Stock Measurement')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure',
                             domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    line_id = fields.Many2one('project.material.line')

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
