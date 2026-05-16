# -*- coding: utf-8 -*-
from odoo import _,api, fields, models
from datetime import datetime

class ProjectProject(models.Model):
    _inherit = 'project.project'

    # project_code = fields.Char(string="Project Code", readonly=True, copy=False)
    #
    # @api.model
    # def create(self, vals):
    #     if not vals.get('project_code'):
    #         year = datetime.now().strftime('%y')  # last 2 digits
    #
    #         seq = self.env['ir.sequence'].next_by_code('project.project') or '0000'
    #
    #         # Extract only number part if prefix exists
    #         number = seq.split('/')[-1]
    #
    #         vals['project_code'] = f"IESI/PROJ/{year}/{number}"
    #
    #     return super(ProjectProject, self).create(vals)


    def action_create_mr(self):
        """Create material request wizard for the current project
        and populate its lines from project material lines."""
        self.ensure_one()  # Make sure this is a single record

        wizard = self.env['material.request.wizard'].create({
            'project_id': self.id,
            # 'task_id': self.id,
        })

        # Prepare wizard lines data
        wizard_lines_data = []
        for line in self.material_line_ids:
            qty_to_deliver = line.quantity - line.done_qty
            if qty_to_deliver > 0:
                wizard_lines_data.append({
                    'wizard_id': wizard.id,
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id,
                    'line_id': line.id,
                })

            line.status = 'mr'
        # Bulk create all wizard lines at once (more efficient)
        if wizard_lines_data:
            self.env['material.wizard.lines'].create(wizard_lines_data)
        return {
            'name': _('Materials'),
            'res_id': wizard.id,
            'type': 'ir.actions.act_window',
            'res_model': 'material.request.wizard',
            'views': [[False, 'form']],
            'view_mode': 'form',
            'target': 'new',
        }


    def action_view_mr(self):
        """View material requests related to the current project."""
        self.ensure_one()
        material_requests = self.env['project.material.request'].search([('project_id', '=', self.id)])
        return {
            'name': _('Material Requests'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.material.request',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', material_requests.ids)],
        }


    # def action_create_purchase(self):
    #     """
    #     Create RFQ creation wizard for the current request
    #     and populate its lines from request lines.
    #     """
    #     self.ensure_one()  # Make sure this is a single record
    #
    #     # Create the wizard
    #     wizard = self.env['rfq.creation.wizard'].create({
    #         'project_id': self.id,
    #         'company_id': self.company_id.id,
    #     })
    #
    #     # Prepare wizard lines data
    #     wizard_lines_data = []
    #     for line in self.material_line_ids:
    #         wizard_lines_data.append({
    #             'rfq_wizard_id': wizard.id,
    #             'product_id': line.product_id.id,
    #             'quantity': line.quantity,
    #             'uom_id': line.uom_id.id,
    #         })
    #
    #     # Bulk create all wizard lines at once (more efficient)
    #     if wizard_lines_data:
    #         self.env['rfq.creation.wizard.lines'].create(wizard_lines_data)
    #     return {
    #         'name': _('Suppliers'),
    #         'res_id': wizard.id,
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'rfq.creation.wizard',
    #         'views': [[False, 'form']],
    #         'view_mode': 'form',
    #         'target': 'new',
    #     }
    #
    # def action_view_delivery_order(self):
    #     self.ensure_one()
    #     delivery_orders = self.env['stock.picking'].search([('picking_type_id.code', '=', 'outgoing')])
    #     print('delivery_orders', delivery_orders)
    #     delivery_orders = delivery_orders.filtered(lambda order: order.project_id.id == self.id)
    #     return {
    #         'name': _('Delivery Orders'),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'stock.picking',
    #         'views': [[False, 'list'], [False, 'form']],
    #         'domain': [('id', 'in', delivery_orders.ids)],
    #     }
    #
    # def action_view_purchases(self):
    #     self.ensure_one()
    #     purchase_orders = self.env['purchase.order'].search([('project_id', '=', self.id)])
    #     return {
    #         'name': _('Purchase Orders'),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'purchase.order',
    #         'views': [[False, 'list'], [False, 'form']],
    #         'domain': [('id', 'in', purchase_orders.ids)],
    #     }
