# -*- coding: utf-8 -*-
from email.policy import default

from odoo import _, api, fields, models

class ProjectMaterialRequest(models.Model):
    _name = 'project.material.request'
    _description = 'Project Material Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True, default='New')
    description = fields.Text(string='Description')
    date = fields.Date(string='Date')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company.id)
    user_id = fields.Many2one(
        "res.users",
        string="Initiated By",
        index=True,
        tracking=True,
        default=lambda self: self.env.user,
    )
    notes = fields.Text("Remarks")
    requested_by = fields.Char(string="Requested By")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'Request to Approve'),
        ('approved', 'Approved'),
    ], string='State', default='draft', tracking=True)

    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         name = rec.name or ''
    #
    #         # Check context from Purchase Order
    #         if self.env.context.get('po_project_name_only'):
    #             display_name = name
    #         else:
    #             if rec.key:
    #                 display_name = f"{rec.key} - {name}"
    #             else:
    #                 display_name = name
    #
    #         result.append((rec.id, display_name))
    #     return result
    project_id = fields.Many2one('project.project', string='Project', required=True)
    task_id = fields.Many2one('project.task', string='Task')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    material_ids = fields.One2many('project.material.request.line', 'request_id', string='Materials')

    prepared_by = fields.Many2one('res.users', string='Prepared By')
    approved_by = fields.Many2one('res.users', string='Approved By')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company.id)

    def _prepare_material_line_from_sale_costing_line(self, line):
        product = line.product_id
        return {
            'product_id': product.product_tmpl_id.id,
            'name': line.name or line.description or product.display_name,
            'quantity': line.quantity,
            'uom_id': line.uom_id.id or product.uom_id.id,
        }

    def _get_material_lines_from_sale_order(self, sale_order):
        return [
            (0, 0, self._prepare_material_line_from_sale_costing_line(line))
            for line in sale_order.sale_costing_lines.filtered('product_id')
        ]

    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        for request in self:
            if request.sale_order_id:
                request.material_ids = [(5, 0, 0)] + request._get_material_lines_from_sale_order(request.sale_order_id)
            else:
                request.material_ids = [(5, 0, 0)]

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'mr.custom.seq'
            ) or _('New')
        if vals.get('sale_order_id') and 'material_ids' not in vals:
            sale_order = self.env['sale.order'].browse(vals['sale_order_id'])
            vals['material_ids'] = self._get_material_lines_from_sale_order(sale_order)
        return super(ProjectMaterialRequest, self).create(vals)

    def action_request_approval(self):
        """Action to change state to 'to_approve'."""
        self.state = 'to_approve'

    def action_approve(self):
        """Approve request and add requested materials to the project."""
        ProjectMaterialLine = self.env['project.material.line']
        for request in self:
            material_lines_vals = []
            request_lines = request.material_ids.filtered(lambda line: not line.project_material_line_id)
            for line in request_lines:
                material_lines_vals.append({
                    'project_id': request.project_id.id,
                    'product_id': line.product_id.id,
                    'quantity': 0,
                    'uom_id': line.uom_id.id,
                    'task_id': line.task_id.id or request.task_id.id,
                    'qty_requested': line.quantity,
                })
            project_material_lines = ProjectMaterialLine.create(material_lines_vals)
            for request_line, project_material_line in zip(request_lines, project_material_lines):
                request_line.project_material_line_id = project_material_line.id
            request.state = 'approved'

    def action_reject(self):
        """Action to change state to 'approved'."""
        self.state = 'draft'

    def write(self, vals):
        """Write records using provided values."""
        if vals.get('sale_order_id') and 'material_ids' not in vals:
            sale_order = self.env['sale.order'].browse(vals['sale_order_id'])
            vals['material_ids'] = [(5, 0, 0)] + self._get_material_lines_from_sale_order(sale_order)
        res = super().write(vals)
        return res
    
    def unlink(self):
        """Delete records"""
        return super().unlink()

    def action_view_purchases(self):
        print()
        self.ensure_one()
        purchase_orders = self.env['purchase.order'].search([('mr_id', '=', self.id)])
        return {
            'name': _('Purchase Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', purchase_orders.ids)],
        }

    def action_view_delivery_order(self):
        print()
        self.ensure_one()
        delivery_orders = self.env['stock.picking'].search(
            [('mr_id', '=', self.id), ('picking_type_id.code', '=', 'outgoing')])
        return {
            'name': _('Delivery Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', delivery_orders.ids)],
        }


    def action_delivery_order(self):
        print('action_delivery_order')
        self.ensure_one()  # Make sure this is a single record

        # Create the wizard
        wizard = self.env['rfq.creation.wizard'].create({
            'project_id': self.project_id.id,
            'company_id': self.company_id.id,
            'mr_id': self.id,
            'dn_bool': True,
        })

        # Prepare wizard lines data
        wizard_lines_data = []
        for line in self.material_ids.filtered(lambda l: l.quantity != l.done_quantity):
            wizard_lines_data.append({
                'rfq_wizard_id': wizard.id,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'uom_id': line.uom_id.id,
                'mr_line_id': line.id,
            })
        # Bulk create all wizard lines at once (more efficient)
        if wizard_lines_data:
            self.env['rfq.creation.wizard.lines'].create(wizard_lines_data)
        return {
            'name': _('Delivery Order'),
            'res_id': wizard.id,
            'type': 'ir.actions.act_window',
            'res_model': 'rfq.creation.wizard',
            'views': [[False, 'form']],
            'view_mode': 'form',
            'target': 'new',
        }

    def action_purchase_order(self):
        print('action_purchase_order')
        self.ensure_one()  # Make sure this is a single record

        # Create the wizard
        wizard = self.env['rfq.creation.wizard'].create({
            'project_id': self.project_id.id,
            'company_id': self.company_id.id,
            'mr_id': self.id,
            'po_bool': True,
        })

        # Prepare wizard lines data
        wizard_lines_data = []
        for line in self.material_ids.filtered(lambda l: l.quantity != l.done_quantity):
            wizard_lines_data.append({
                'rfq_wizard_id': wizard.id,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'uom_id': line.uom_id.id,
                'mr_line_id': line.id,
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


class ProjectMaterialRequestLine(models.Model):
    _name = 'project.material.request.line'
    _description = 'Project Material Request Line'

    name = fields.Char(string='Description')
    task_id = fields.Many2one('project.task')
    product_id = fields.Many2one('product.template', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    request_id = fields.Many2one('project.material.request', string='Material Request', required=True)
    status = fields.Selection([
        ('to_delivered', 'To Deliver'),
        ('po', 'PO'),
        ('dn', 'DN'),], string='Status', default='to_delivered', required=True)
    project_material_line_id = fields.Many2one('project.material.line', string='Project Material Line')
    done_quantity = fields.Float(string='Done Quantity', compute='_compute_done_quantity', store=True)
    po_ids = fields.Many2many('purchase.order', string='Purchase Orders')
    dn_ids = fields.Many2many('stock.picking', string='Delivery Orders')

    @api.depends('dn_ids')
    def _compute_done_quantity(self):
        for line in self:
            line.done_quantity = 0

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
