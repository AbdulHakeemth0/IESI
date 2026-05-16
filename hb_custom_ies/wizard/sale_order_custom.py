from odoo import models, fields,api

class SaleReturnWizard(models.TransientModel):
    _name = 'sale.return.wizard'

    reason = fields.Text(required=True)

    def action_submit(self):
        order = self.env['sale.order'].browse(self.env.context.get('active_id'))

        order.write({
            'state': 'draft',
            'return_reason': self.reason,
            'is_returned': True,
        })
        return {'type': 'ir.actions.act_window_close'}
