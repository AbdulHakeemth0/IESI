from odoo import models, fields, api

class SunItems(models.Model):
    _name ='sun.items'
    _description = 'Sun Items'

    line_id = fields.Many2one('sale.order', string="Sundering")
    sun_items =fields.Many2one('sundering',string='Items')
    sun_qty_item = fields.Float(string="Qty", digits=(16, 3))
    sun_unit_price_item = fields.Float(string="Unit Price", digits=(16, 3))
    sun_amount_item = fields.Float(
        string="Amount",
        compute='_compute_sun_amount_item',
        store=True,
        digits=(16, 3)
    )

    @api.depends('sun_qty_item', 'sun_unit_price_item')
    def _compute_sun_amount_item(self):
        for line in self:
            qty = line.sun_qty_item if line.sun_qty_item else 0.0
            price = line.sun_unit_price_item if line.sun_unit_price_item else 0.0
            line.sun_amount_item = qty * price