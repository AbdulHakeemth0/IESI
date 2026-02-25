from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'


    cr_no = fields.Char(string='CR No')
    fax_no = fields.Char(string='Fax No')
