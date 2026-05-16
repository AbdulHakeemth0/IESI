from odoo import models, fields, api

class SaleGeneral(models.Model):
    _name ='sale.general'
    _description = 'General'

    line_id = fields.Many2one('sale.order', string="Sundering")
    gen_item = fields.Char(string='General Item')
    gen_qty_item = fields.Float(string='General Qty', digits=(16, 3))
    gen_unit_price_item = fields.Float(string='General Unit Price', digits=(16, 3))
    gen_amount_item = fields.Float(
        string='General Amount',
        compute='_compute_gen_amount_item',
        store=True,
        digits=(16, 3)
    )

    @api.depends('gen_qty_item', 'gen_unit_price_item')
    def _compute_gen_amount_item(self):
        for line in self:
            qty = line.gen_qty_item if line.gen_qty_item else 0.0
            price = line.gen_unit_price_item if line.gen_unit_price_item else 0.0
            line.gen_amount_item = qty * price