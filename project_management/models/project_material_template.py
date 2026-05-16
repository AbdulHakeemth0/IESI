from odoo import models, fields, api

class ProjectMaterialTemplate(models.Model):
    _name = 'project.material.template'
    _description = 'Project Material Template'

    name = fields.Char(required=True)
    line_ids = fields.One2many(
        'project.material.template.line',
        'template_id',
        string='Materials'
    )
    project_discipline_id = fields.Many2one('project.discipline', required=True)

class ProjectMaterialTemplateLine(models.Model):
    _name = 'project.material.template.line'
    _description = 'Project Material Template Line'

    template_id = fields.Many2one(
        'project.material.template',
        required=True,
        ondelete='cascade'
    )
    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Float(default=1.0)
    is_material = fields.Boolean(string='Is Material', readonly=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure',
                             domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
            if self.product_id.type != 'service':
                self.is_material = True
            else:
                self.is_material = False
