from odoo import models, fields,api

class ModePayment(models.Model):
    _name = 'mode.payment'
    _description = 'Mode Payment'
    _rec_name = 'm_name'

    m_name = fields.Char(string='Mode Payment', required=True)




class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    mode_ids = fields.Many2one('mode.payment', string='Mode of Payment', copy=True)
    scope = fields.Char(string="Scope")
    payment_terms = fields.Many2one('account.payment.term', string="Payment Terms")
    quote_date = fields.Date(string="Quote Date", default=fields.Date.today)
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True
    )

