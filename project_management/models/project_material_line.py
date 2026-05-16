# -*- coding: utf-8 -*-
from odoo import api, fields, models ,_
from odoo.api import readonly
from odoo.exceptions import ValidationError



class ProjectMaterialLine(models.Model):
    """ This model represents project.material.line."""
    _name = 'project.material.line'
    _description = 'ProjectMaterialLine'

    project_id = fields.Many2one('project.project', string='Project', required=True,
                                 ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    task_id = fields.Many2one('project.task', string='Task', domain="[('project_id', '=', project_id)]")
    status = fields.Selection([
        ('to_delivered', 'To Deliver'),
        ('mr', 'Mr Created'),
        ('partial_delivery', 'Partial Delivery'),
        ('delivered', 'Delivered'),
    ], string='Status', default='to_delivered', required=True, compute='_compute_status')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    move_ids = fields.Many2many('stock.move', 'material_line_stock_move_rel', string='Stock Moves')
    done_qty = fields.Float(string='Done Quantity', compute='_compute_done_qty')
    qty_remaining = fields.Float(string="Remaining Qty", compute="_compute_remaining_qty",
                                 store=True)
    # qty_requested = fields.Float(string="Requested Qty")
    qty_requested = fields.Float(string="Requested Qty", readonly=True)

    @api.onchange('quantity')
    def onchange_quantity(self):
        if self.qty_remaining < 0:
            raise ValidationError(
                          _("Quantity exceeds remaining quantity."))
        # if self.quantity > self.qty_remaining:
        #     raise ValidationError(
        #         _("Total with Margin for Fire Alarm must be equal to the Untaxed Amount."))

    @api.depends('quantity', 'done_qty')
    def _compute_remaining_qty(self):
        for rec in self:
            # rec.qty_remaining = max(rec.quantity - rec.done_qty, 0)
            rec.qty_remaining = rec.qty_requested - rec.quantity

    @api.depends('move_ids.state')
    def _compute_done_qty(self):
        for rec in self:
            rec.done_qty = 0
            if rec.move_ids:
                done_moves = rec.move_ids.filtered(lambda m: m.state == 'done')
                if done_moves:
                    qty = sum(done_moves.mapped('quantity'))
                    rec.done_qty = qty

    @api.depends('done_qty', 'quantity', 'qty_requested')
    def _compute_status(self):
        for rec in self:
            rec.status = 'to_delivered'
            if rec.done_qty >= rec.quantity:
                rec.status = 'delivered'
            else:
                if rec.qty_requested > 0:
                    rec.status = 'mr'
                if rec.done_qty > 0:
                    rec.status = 'partial_delivery'

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
