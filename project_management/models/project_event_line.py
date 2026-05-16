# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.api import readonly


class ProjectEventLine(models.Model):
    """ This model represents project.material.line."""
    _name = 'project.event.line'
    _description = 'ProjectEventLine'

    project_id = fields.Many2one('project.project', string='Project', required=True,
                                 ondelete='cascade')
    event_id = fields.Many2one('project.event', string='Event', ondelete='cascade')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    description = fields.Char(string='Description')
