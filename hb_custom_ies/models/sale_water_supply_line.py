# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleWaterSupplyLine(models.Model):
    """ This model represents sale.water.supply.line."""
    _name = 'sale.water.supply.line'
    _description = 'SaleWaterSupplyLine'

    line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    water_supply_item_id = fields.Many2one('water.supply', string='Item', required=True)
    quantity = fields.Float(string='Quantity')
    description = fields.Text(string='Description')
    unit_price = fields.Float(string='Unit Price', related='water_supply_item_id.water_unit_rate')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price
