# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleFireFightingLine(models.Model):
    """ This model represents sale.fire.fighting.line."""
    _name = 'sale.fire.fighting.line'
    _description = 'SaleFireFightingLine'

    line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    fire_fighting_item_id = fields.Many2one('fire.fighting.item', string='Item', required=True)
    quantity = fields.Float(string='Quantity')
    description = fields.Text(string='Description')
    unit_price = fields.Float(string='Unit Price', related='fire_fighting_item_id.fire_fighting_unit_rate')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price
