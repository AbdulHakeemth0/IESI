# -*- coding: utf-8 -*-
from odoo import _,api, fields, models
from odoo.api import ValuesType


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_project_prepare_values(self):
        """Generate project values"""
        scope_type = False
        if self.order_id.is_fire_alarm:
            scope_type = 'fire_alarm'
        if self.order_id.is_fire_fighting:
            scope_type = 'fire_fighting'
        if self.order_id.is_elv:
            scope_type = 'elv'
        if self.order_id.is_civil:
            scope_type = 'civil'
        if self.order_id.is_water_supply:
            scope_type = 'water_supply'
        if self.order_id.is_drainage:
            scope_type = 'drainage'
        if self.order_id.is_plumbing:
            scope_type = 'plumbing'
        if self.order_id.is_electrical:
            scope_type = 'electrical'
        if self.order_id.is_hvac:
            scope_type = 'hvac'
        if self.order_id.is_mep:
            scope_type = 'mep'

        materials_list = []

        line_fields = [
            'sale_costing_lines',
            'plumbing_costing_lines',
            'water_supply_costing_lines',
            'fire_alarm_costing_lines',
            'fire_fighting_costing_lines',
            'drainage_costing_lines',
            'civil_costing_lines',
            'elv_costing_lines',
            'mep_costing_lines',
            'hvac_costing_lines',
        ]

        all_lines = self.env['sale.costing.line']

        for field in line_fields:
            all_lines |= self.order_id[field]

        for line in all_lines.filtered(lambda l: l.is_material):
            materials_list.append({
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'uom_id': line.uom_id.id,
            })

        # create the project or duplicate one
        return {
            'name': '%s - %s' % (self.order_id.client_order_ref, self.order_id.name) if self.order_id.client_order_ref else self.order_id.name,
            'account_id': self.env.context.get('project_account_id') or self.order_id.project_account_id.id or self.env['account.analytic.account'].create(self.order_id._prepare_analytic_account_data()).id,
            'partner_id': self.order_id.partner_id.id,
            'sale_line_id': self.id,
            'active': True,
            'company_id': self.company_id.id,
            'allow_billable': True,
            'user_id': self.product_id.project_template_id.user_id.id,
            'scope_type': scope_type,
            'project_type': self.order_id.project_type,
            'project_discipline_ids': self.order_id.project_discipline_ids.ids,
            'material_line_ids': [(0, 0, material) for material in materials_list],
        }
