# -*- coding: utf-8 -*-
from typing import Self

from odoo import _,api, fields, models
from odoo.api import ValuesType


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.depends('name', 'project_sequence', 'sale_order_id.project_name')
    def _compute_display_name(self):

        super()._compute_display_name()

        if not self.env.context.get('material_request_display'):
            return

        for rec in self:

            sale_project_name = rec.sale_order_id.project_name or ''
            sequence = rec.project_sequence or ''
            name = rec.name or ''

            if sale_project_name and sequence:
                rec.display_name = f'[{sale_project_name}] {sequence}'

            elif sequence:
                rec.display_name = sequence

            else:
                rec.display_name = name
            # if rec.project_sequence:
            #     rec.display_name = rec.project_sequence
            # else:
            #     rec.display_name = rec.name or ''

    # def name_get(self):
    #     result = []
    #     print('workingggg')
    #     for rec in self:
    #         print(rec,"ddssdsds")
    #         if self.env.context.get('project_name_only'):
    #             name = rec.name or ''
    #         else:
    #             if rec.project_sequence:
    #                 name = f"{rec.project_sequence}"
    #             else:
    #                 name = rec.name or ''
    #         result.append((rec.id, name))
    #     return result

    project_type = fields.Selection([
        ('design', 'Design'),
        ('design_build', 'Design & Build'),
        ('installation', 'Installation'),
        ('project_management', 'Project Management'),
        ('maintenance', 'Maintenance'),
        ('supply', 'Supply'),
        ('civil', 'Civil'),
        ('interior', 'Interior'),
        ('supply and installation', 'Supply and Installation'),
    ], string="Project Type", copy=True)

    scope_type = fields.Selection([
        ('mep', 'MEP'),
        ('hvac', 'HVAC'),
        ('mep_hvac', 'MEP & HVAC'),
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('water_supply', 'Water Supply'),
        ('drainage', 'Drainage'),
        ('civil', 'Civil'),
        ('elv', 'ELV'),
        ('fire_fighting', 'Fire Fighting'),
        ('fire_alarm', 'Fire Alarm'),
    ], string="Discipline", copy=True)

    material_line_ids = fields.One2many('project.material.line', 'project_id', string="Material Lines")
    material_template_id = fields.Many2one('project.material.template', string="Material Template")
    project_event_line_ids = fields.One2many('project.event.line', 'project_id', string="Project Events")
    project_sequence = fields.Char(string='Number', copy=False, readonly=True, default='New')
    no_of_days = fields.Integer(string="No of Days", compute='_compute_no_of_days')
    project_discipline_ids = fields.Many2many('project.discipline', 'project_project_discipline_ids_rel')

    @api.depends('date_start', 'date')
    def _compute_no_of_days(self):
        for project in self:
            if project.date_start and project.date:
                start_date = fields.Date.from_string(project.date_start)
                end_date = fields.Date.from_string(project.date)
                project.no_of_days = (end_date - start_date).days + 1
            else:
                project.no_of_days = 0

    @api.model
    def create(self, vals):
        if vals.get('project_sequence', 'New') == 'New':
            vals['project_sequence'] = self.env['ir.sequence'].next_by_code('project.custom.seq') or 'New'
        return super(ProjectProject, self).create(vals)

    @api.onchange('material_template_id')
    def _onchange_material_template_id(self):
        if self.material_template_id:
            lines = []
            for line in self.material_template_id.line_ids:
                lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id or line.product_id.uom_id.id,
                }))
            self.material_line_ids = lines

    def action_create_purchase(self):
        """
        Create RFQ creation wizard for the current request
        and populate its lines from request lines.
        """
        self.ensure_one()  # Make sure this is a single record

        # Create the wizard
        wizard = self.env['rfq.creation.wizard'].create({
            'project_id': self.id,
            'company_id': self.company_id.id,
        })

        # Prepare wizard lines data
        wizard_lines_data = []
        for line in self.material_line_ids:
            wizard_lines_data.append({
                'rfq_wizard_id': wizard.id,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'uom_id': line.uom_id.id,
            })

        # Bulk create all wizard lines at once (more efficient)
        if wizard_lines_data:
            self.env['rfq.creation.wizard.lines'].create(wizard_lines_data)
        return {
            'name': _('Suppliers'),
            'res_id': wizard.id,
            'type': 'ir.actions.act_window',
            'res_model': 'rfq.creation.wizard',
            'views': [[False, 'form']],
            'view_mode': 'form',
            'target': 'new',
        }

    def action_view_delivery_order(self):
        self.ensure_one()
        delivery_orders = self.env['stock.picking'].search([('picking_type_id.code', '=', 'outgoing')])
        print('delivery_orders', delivery_orders)
        delivery_orders = delivery_orders.filtered(lambda order: order.project_id.id == self.id)
        return {
            'name': _('Delivery Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', delivery_orders.ids)],
        }

    def action_view_purchases(self):
        self.ensure_one()
        purchase_orders = self.env['purchase.order'].search([('project_id', '=', self.id)])
        return {
            'name': _('Purchase Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', purchase_orders.ids)],
        }



    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         if self.env.context.get('po_project_name_only'):
    #             name = rec.name or ''
    #         else:
    #             if rec.key:
    #                 name = f"{rec.key} - {rec.name}"
    #             else:
    #                 name = rec.name or ''
    #         result.append((rec.id, name))
    #     return result