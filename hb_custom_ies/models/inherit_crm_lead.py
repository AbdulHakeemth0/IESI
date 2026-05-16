from odoo import models, fields, api, _

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    seq_no = fields.Char(
        string="Sequence No",
        readonly=True,
        copy=False,
        default="New"
    )
    reference = fields.Char(string="Reference", copy=True)
    location= fields.Char(string='Location', copy=True)
    address = fields.Char(string='Address')
    project_type = fields.Selection([
        ('design', 'Design'),
        ('design_build', 'Design & Build'),
        ('installation', 'Installation'),
        ('project_management', 'Project Management'),
        ('maintenance', 'Maintenance'),
        ('supply', 'Supply of Labour'),
        ('civil', 'Civil Works'),
        ('interior', 'Interior'),
        ('supply and installation', 'Supply of Material'),
    ], string="Project Type", copy=True)
    scope_title = fields.Char(string="Scope Title", copy=True)
    color = fields.Integer('Color Index', default=0)
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
    project_discipline_ids = fields.Many2many('project.discipline', 'crm_project_discipline_ids_rel')

    @api.model
    def create(self, vals):
        if vals.get('seq_no', 'New') == 'New':
            vals['seq_no'] = self.env['ir.sequence'].next_by_code(
                'crm.lead.iesi'
            ) or _('New')
        return super(CrmLead, self).create(vals)


    def action_new_quotation(self):
        action = super().action_new_quotation()
        action['context']['default_project_name'] = self.id
        action['context']['default_project_name'] = self.id
        if self.project_discipline_ids:
            action['context']['default_project_discipline_ids'] = self.project_discipline_ids.ids
        return action

    @api.onchange('partner_id')
    def onchange_partner_id_custom(self):
        if self.partner_id:
            self.address = self.partner_id.contact_address

