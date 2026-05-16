# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api, fields, models


class SaleCostingLine(models.Model):
    """ This model represents sale.costing.line."""
    _name = 'sale.costing.line'
    _description = 'SaleCostingLine'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_plumbing_line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_water_supply_line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_fire_alarm_line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_fire_fighting_line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_drainage_line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_civil_line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_elv_line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_mep_line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sale_hvac_line_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Items')
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    description = fields.Text(string='Description')
    currency_id = fields.Many2one('res.currency', string='Currency', related="sale_order_id.currency_id")
    unit_price = fields.Monetary(string='Unit Price')
    is_material = fields.Boolean(string='Is Material')
    total_price = fields.Monetary(string='Total Price', compute='_compute_total_price', store=True)
    name = fields.Char('Description')
    display_type = fields.Selection(
        selection=[
            ('line_section', "Section"),
            ('line_note', "Note"),
        ],
        default=False)


    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for line in self:
            line.total_price = line.quantity * line.unit_price

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
            self.unit_price = self.product_id.list_price
