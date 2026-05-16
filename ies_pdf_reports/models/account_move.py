from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    description = fields.Char(string="Description")




class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    custom_description = fields.Html(string="Custom Description")


class AccountMove(models.Model):
    _inherit = 'account.move'

    agreed_amount = fields.Monetary(string="Agreed Amount")
    additional_work = fields.Monetary(string="Additional Work")
    received_amount = fields.Monetary(string="Received Amount")
    project_name = fields.Char(string='Project Name')
    claim_amount = fields.Monetary(string="Claim Amount")
    vat_amount = fields.Monetary(string="VAT(5%)", compute='_compute_vat_amount')
    total_amount = fields.Monetary(string='Total Amount' , compute='_compute_total_amount')

    @api.depends('claim_amount')
    def _compute_vat_amount(self):
        for rec in self:
            rec.vat_amount = (rec.claim_amount or 0.0) * 0.05

    @api.depends('additional_work', 'received_amount', 'claim_amount', 'vat_amount')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = (
                    (rec.claim_amount or 0.0) +
                    (rec.vat_amount or 0.0)
            )

    # claim_amount = fields.Monetary(string="Claim Amount", compute="_compute_amounts", store=True)
    # vat_amount = fields.Monetary(string="VAT Amount", compute="_compute_amounts", store=True)
    # total_amount = fields.Monetary(string="Total Amount", compute="_compute_amounts", store=True)
    #
    # balance_amount = fields.Monetary(string="Balance Amount", compute="_compute_balance", store=True)
    #
    # currency_id = fields.Many2one(
    #     'res.currency',
    #     default=lambda self: self.env.company.currency_id
    # )
    #
    # @api.depends('agreed_amount', 'additional_work', 'received_amount')
    # def _compute_amounts(self):
    #     for rec in self:
    #         agreed = rec.agreed_amount or 0.0
    #         additional = rec.additional_work or 0.0
    #         received = rec.received_amount or 0.0
    #
    #         # Claim
    #         claim = (agreed + additional) - received
    #         rec.claim_amount = max(claim, 0.0)
    #
    #         # VAT only on agreed_amount and additional_work
    #         rec.vat_amount = (agreed + additional) * 0.05
    #
    #         # Total = agreed + additional + VAT
    #         rec.total_amount = agreed + additional + rec.vat_amount
    #
    # @api.depends('total_amount', 'received_amount')
    # def _compute_balance(self):
    #     for rec in self:
    #         total = rec.total_amount or 0.0
    #         received = rec.received_amount or 0.0
    #
    #         rec.balance_amount = total - received