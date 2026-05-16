from odoo import models, fields

class PlanningTemplate(models.Model):
    _inherit = "planning.slot"

    activity = fields.Text(string="Activity")
    remarks = fields.Char(string="Remarks")

    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         # If context key is set, show only project name
    #         if self.env.context.get('po_project_id_only'):
    #             name = rec.project_id.name if rec.project_id else ''
    #         else:
    #             # Normal display: key - name
    #             if rec.key:1
    #                 name = f"{rec.key} - {rec.name or ''}"
    #             else:
    #                 name = rec.name or ''
    #         result.append((rec.id, name))
    #     return result