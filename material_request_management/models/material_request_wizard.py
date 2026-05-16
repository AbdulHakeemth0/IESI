from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class MaterialRequestWizard(models.TransientModel):
    _inherit = "material.request.wizard"

    def action_create_mr(self):
        """Create material request wizard for the current project"""
        if not self.material_ids:
            raise ValidationError(_('Please add at least one material line.'))
        if not sum(self.material_ids.mapped('quantity')) > 0:
            raise ValidationError(_('Please add quantity for at least one material line.'))
        request = self.env['project.material.request'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'company_id': self.project_id.company_id.id,
        })
        for line in self.material_ids:
            self.env['project.material.request.line'].create({
                'product_id': line.product_id.id,
                'name': line.product_id.name,
                'quantity': line.quantity,
                'uom_id': line.uom_id.id,
                'project_material_line_id': line.line_id.id,
                'task_id': self.task_id.id,
                'request_id': request.id
            })
            line.line_id.qty_requested += line.quantity
        return {
            'name': _('Material Request'),
            'res_id': request.id,
            'type': 'ir.actions.act_window',
            'res_model': 'project.material.request',
            'views': [[False, 'form']],
            'view_mode': 'form',
            'target': 'current',
        }
