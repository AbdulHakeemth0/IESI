from odoo import models, fields, api

class SaleMeasurement(models.Model):
    _name ='sale.measurement'
    _description = 'Measurement'

    line_id = fields.Many2one('sale.order', string="Sundering")
    items = fields.Char(string='Items')
    width = fields.Float(string='Width', digits=(16, 3))
    depth = fields.Float(string='Depth', digits=(16, 3))
    length = fields.Float(stringh='Length', digits=(16, 3))
    total_area = fields.Float(
        string='Total Area',
        digits=(16, 3),
        compute='_compute_total_area',
        readonly=True
    )

    @api.depends('width', 'depth', 'length')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = (2 * (rec.width + rec.depth)) * rec.length


class Measurement(models.Model):
    _name = 'mesurement.measurement'
    _description = 'Measurement'

    line_id = fields.Many2one('sale.order', string="Measurement")   # REQUIRED

    items_measurement = fields.Char(string='Items')
    items_unit = fields.Many2one('uom.uom',string='Units')
    length_measurement = fields.Float(string='Quantity', digits=(16, 3))