from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'


    cr_no = fields.Char(string='CR No')
    # extract_in_invoice_digitalization_mode = fields.Selection(
    #     selection_add=[('manual', 'Manual')],
    # )
    # extract_out_invoice_digitalization_mode = fields.Selection(
    #     selection_add=[('manual', 'Manual')],
    # )
    # fax_no = fields.Char(string='Fax No')
