# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

class RfqCreationWizardLines(models.TransientModel):
    _name = "rfq.creation.wizard.lines"
    _description = "Purchase RFQ Creation Wizard"

    rfq_wizard_id = fields.Many2one('rfq.creation.wizard', readonly=1)
    product_id = fields.Many2one('product.product')
    quantity = fields.Float(string="Quantity to purchase", digits='Stock Measurement')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True,
                             domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
