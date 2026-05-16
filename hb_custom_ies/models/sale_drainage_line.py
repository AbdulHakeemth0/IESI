# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleDrainageLine(models.Model):
    """ This model represents sale.drainage.line."""
    _name = 'sale.drainage.line'
    _description = 'SaleDrainageLine'

    line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    drainage_item_id = fields.Many2one('drainage.item', string='Item', required=True)
    quantity = fields.Float(string='Quantity')
    description = fields.Text(string='Description')
    unit_price = fields.Float(string='Unit Price', related='drainage_item_id.drainage_unit_rate')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price
