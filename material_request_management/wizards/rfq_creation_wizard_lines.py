# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

class RfqCreationWizardLines(models.TransientModel):
    _inherit = "rfq.creation.wizard.lines"

    mr_line_id = fields.Many2one('project.material.request.line', string='Material Request Line')


class RfqCreationWizard(models.TransientModel):
    """Rfq Creation Wizard"""
    _inherit = "rfq.creation.wizard"

    mr_id = fields.Many2one('project.material.request', string='Material Request')
