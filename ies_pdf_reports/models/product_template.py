from odoo import models, api, fields
import re
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'



    _sql_constraints = [
        (
            'default_code_unique',
            'unique(default_code)',
            'Product Code must be unique!'
        )
    ]

    @api.model
    def create(self, vals):
        # Generate sequence
        if not vals.get('default_code') or vals.get('default_code') == 'New':
            vals['default_code'] = self.env['ir.sequence'].next_by_code(
                'product.code.sequence'
            ) or '0000'

        product_name = vals.get('name', '') or ''
        default_code = vals.get('default_code', '') or ''

        product_name = re.sub(r'^\[[^\]]+\]\s*-\s*', '', product_name).strip()

        # Set clean name
        vals['name'] = '[%s] - %s' % (
            default_code,
            product_name
        )

        return super(ProductTemplate, self).create(vals)

    @api.depends('name', 'default_code')
    def _compute_display_name(self):
        for product in self:
            # name already formatted aanu
            print("dddddddddd")
            product.display_name = product.name or ''


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.depends('name', 'default_code')
    def _compute_display_name(self):
        for product in self:
            # name already contains code
            product.display_name = product.name or ''