# -*- coding: utf-8 -*-
from odoo import _,api, fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    material_line_ids = fields.One2many(
        'project.material.line',
        'task_id',
        string="Material Lines"
    )

    no_of_days = fields.Integer(
        string="No of Days",
        compute='_compute_no_of_days',
        store=True
    )

    project_type = fields.Selection([
        ('design', 'Design'),
        ('design_build', 'Design & Build'),
        ('installation', 'Installation'),
        ('project_management', 'Project Management'),
        ('maintenance', 'Maintenance'),
        ('supply', 'Supply'),
        ('civil', 'Civil'),
        ('interior', 'Interior'),
        ('supply_installation', 'Supply and Installation'),  # ✅ fixed key (no space)
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

    project_discipline_ids = fields.Many2many(
        'project.discipline',
        'project_project_discipline_rel',  # ✅ corrected relation table name
        'task_id',
        'discipline_id',
        string="Project Disciplines"
    )
    material_template_id = fields.Many2one('project.material.template', string="Material Template")


    @api.depends('planned_date_start', 'date_deadline')
    def _compute_no_of_days(self):
        for task in self:
            if task.planned_date_start and task.date_deadline:
                start_date = fields.Date.from_string(task.planned_date_start)
                end_date = fields.Date.from_string(task.date_deadline)
                task.no_of_days = (end_date - start_date).days + 1
            else:
                task.no_of_days = 0


    def action_material_request(self):
        """
        Create material request wizard for the current request
        and populate its lines from request lines.
        """
        self.ensure_one()  # Make sure this is a single record

        # Create the wizard
        wizard = self.env['material.request.wizard'].create({
            'project_id': self.project_id.id,
            'task_id': self.id,
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
        # Bulk create all wizard lines at once (more efficient)
        if wizard_lines_data:
            self.env['material.wizard.lines'].create(wizard_lines_data)
        return {
            'name': _('Material'),
            'res_id': wizard.id,
            'type': 'ir.actions.act_window',
            'res_model': 'material.request.wizard',
            'views': [[False, 'form']],
            'view_mode': 'form',
            'target': 'new',
        }

    def action_view_material_request(self):
        self.ensure_one()
        delivery_orders = self.env['stock.picking'].search(
            [('picking_type_id.code', '=', 'outgoing')])
        print('delivery_orders', delivery_orders)
        delivery_orders = delivery_orders.filtered(lambda order: order.project_id.id == self.project_id.id and order.task_id.id == self.id)
        return {
            'name': _('Delivery Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', delivery_orders.ids)],
        }
