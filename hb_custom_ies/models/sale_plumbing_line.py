# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SalePlumbingLine(models.Model):
    """ This model represents sale.plumbing.line."""
    _name = 'sale.plumbing.line'
    _description = 'SalePlumbingLine'

    line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    plumbing_item_id = fields.Many2one('plumbing', string='Item', required=True)
    quantity = fields.Float(string='Quantity')
    description = fields.Text(string='Description')
    unit_price = fields.Float(string='Unit Price', related='plumbing_item_id.plumbing_unit_rate')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price
