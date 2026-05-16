# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProjectDiscipline(models.Model):
    """ This model represents project.discipline."""
    _name = 'project.discipline'
    _description = 'ProjectDiscipline'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer('Color Index', default=0)
