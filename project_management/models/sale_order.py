# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    material_template_ids = fields.Many2many('project.material.template',
                                             'sale_project_material_template_rel',
                                             string="Material Template")

    @api.onchange('material_template_ids')
    def _onchange_sale_material_template_id(self):
        print('_onchange_sale_material_template_id')
        self.sale_costing_lines = [(5, 0, 0)]
        self.plumbing_costing_lines = [(5, 0, 0)]
        self.water_supply_costing_lines = [(5, 0, 0)]
        self.fire_alarm_costing_lines = [(5, 0, 0)]
        self.fire_fighting_costing_lines = [(5, 0, 0)]
        self.drainage_costing_lines = [(5, 0, 0)]
        self.civil_costing_lines = [(5, 0, 0)]
        self.elv_costing_lines = [(5, 0, 0)]
        self.mep_costing_lines = [(5, 0, 0)]
        self.hvac_costing_lines = [(5, 0, 0)]
        if not self.material_template_ids:
            return
        discipline_map = {
            'electrical_discipline_id': 'sale_costing_lines',
            'plumbing_discipline_id': 'plumbing_costing_lines',
            'water_supply_discipline_id': 'water_supply_costing_lines',
            'fire_alarm_discipline_id': 'fire_alarm_costing_lines',
            'fire_fighting_discipline_id': 'fire_fighting_costing_lines',
            'drainage_discipline_id': 'drainage_costing_lines',
            'civil_discipline_id': 'civil_costing_lines',
            'elv_discipline_id': 'elv_costing_lines',
            'mep_discipline_id': 'mep_costing_lines',
            'hvac_discipline_id': 'hvac_costing_lines',
        }

        for discipline_field, line_field in discipline_map.items():
            discipline = self[discipline_field]
            if not discipline:
                continue

            template = self.material_template_ids.filtered(
                lambda x: x.project_discipline_id.id == discipline.id
            )

            lines = []
            for line in template.mapped('line_ids'):
                lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id or line.product_id.uom_id.id,
                    'unit_price': line.product_id.list_price,
                    'is_material': line.is_material,
                }))
            self[line_field] = lines
