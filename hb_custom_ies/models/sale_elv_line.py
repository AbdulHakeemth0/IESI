# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleELVlLine(models.Model):
    """ This model represents sale.civil.line."""
    _name = 'sale.elv.line'
    _description = 'SaleELVLine'

    line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    elv_item_id = fields.Many2one('elv.item', string='Item', required=True)
    quantity = fields.Float(string='Quantity')
    description = fields.Text(string='Description')
    unit_price = fields.Float(string='Unit Price', related='elv_item_id.elv_unit_rate')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price
