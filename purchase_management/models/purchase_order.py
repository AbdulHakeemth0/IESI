# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, Command, fields, models
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    approved_bool = fields.Boolean()
    approve_requested = fields.Boolean()
    state = fields.Selection(selection_add=[
        ("to_approve", "Waiting Approval"),
        ("rejected", "Rejected")
    ])

    def action_request_approve(self):
        print('action_request_approve')
        self.approve_requested = True
        self.state = "to_approve"

    def action_approve(self):
        print('action_approve')
        self.approved_bool = True
        self.state = "draft"

