from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'


    cr_no = fields.Char(string='CR No')



# from odoo import models, fields, api
#
# class CrmLead(models.Model):
#     _inherit = 'crm.lead'
#
#     street = fields.Char(string="Street")
#     street2 = fields.Char(string="Street2")
#     city = fields.Char(string="City")
#     state_id = fields.Many2one('res.country.state', string="State")
#     zip = fields.Char(string="ZIP")
#     country_id = fields.Many2one('res.country', string="Country")
#
#     @api.onchange('partner_id')
#     def _onchange_partner_id_address(self):
#         if self.partner_id:
#             self.street = self.partner_id.street
#             self.street2 = self.partner_id.street2
#             self.city = self.partner_id.city
#             self.state_id = self.partner_id.state_id
#             self.zip = self.partner_id.zip
#             self.country_id = self.partner_id.country_id