# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProjectEvent(models.Model):
    """ This model represents project.event."""
    _name = 'project.event'
    _description = 'ProjectEvent'

    name = fields.Char(string='Event Name', required=True)
