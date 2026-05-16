from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    mr_id = fields.Many2one('project.material.request', string="MR")
