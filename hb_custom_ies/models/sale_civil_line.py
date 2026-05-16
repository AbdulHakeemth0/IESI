# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleCivilLine(models.Model):
    """ This model represents sale.civil.line."""
    _name = 'sale.civil.line'
    _description = 'SaleCivilLine'

    line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    civil_item_id = fields.Many2one('civil.item', string='Item', required=True)
    quantity = fields.Float(string='Quantity')
    description = fields.Text(string='Description')
    unit_price = fields.Float(string='Unit Price', related='civil_item_id.civil_unit_rate')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price
