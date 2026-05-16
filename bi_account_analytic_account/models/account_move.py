from typing import Sequence

from odoo import api, fields, models,_
from datetime import date
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    type = fields.Selection([
        ('project', 'Project'),
        ('trading', 'Trading'),
        ('maintenance', 'Maintenance'),
    ], string="Type")

    expected_currency_rate = fields.Float(string="Expected Currency Rate")
    # invoicing_percentage = fields.Float(string="Invoicing Percentage",tracking=True)
    acc_type = fields.Selection([
        ('BANK', 'BANK'),
        ('CASH', 'CASH'),
        ('JOURNAL','JOURNAL'),
    ], string="Account Type")
    
    lpo_no = fields.Char(
        string='LPO No',
    )
    sequence_no = fields.Char('Sequence No.',copy=False, default=lambda self: _('New'))
    # adv_amount_received = fields.Float(
    #     string='Advance Amount Received',
    # )

    def _valid_field_parameter(self, field, name):
        # EXTENDS models
        return name == 'tracking' or super()._valid_field_parameter(field, name)

    # @api.model_create_multi
    # def create(self, vals_list):
    #     records = super().create(vals_list)
    #
    #     trading_journal = self.env['account.journal'].sudo().search(
    #         [('p_t_m_type', '=', 'trading')], limit=1)
    #
    #     project_journal = self.env['account.journal'].sudo().search(
    #         [('p_t_m_type', '=', 'project')], limit=1)
    #
    #     maintenance_journal = self.env['account.journal'].sudo().search(
    #         [('p_t_m_type', '=', 'maintenance')], limit=1)
    #
    #     for rec in records:
    #
    #
    #
    #         if rec.type == 'project':
    #             rec.sequence_no = self.env['ir.sequence'].next_by_code('account.move.seq') or _("New")
    #             rec.journal_id = project_journal.id
    #
    #         elif rec.type == 'trading':
    #             rec.sequence_no = self.env['ir.sequence'].next_by_code('account.move.tra') or _("New")
    #             rec.journal_id = trading_journal.id
    #
    #         elif rec.type == 'maintenance':
    #             rec.sequence_no = self.env['ir.sequence'].next_by_code('account.move.main') or _("New")
    #             rec.journal_id = maintenance_journal.id
    #
    #     return records



    @api.onchange('type')
    def _onchange_type_amc_vas(self):
        trading_journal = self.env['account.journal'].sudo().search([('p_t_m_type', '=', 'trading')])
        project_journal = self.env['account.journal'].sudo().search([('p_t_m_type', '=', 'project')])
        maintenance_journal = self.env['account.journal'].sudo().search([('p_t_m_type', '=', 'maintenance')])
        if self.type == 'project' and project_journal:
            self.journal_id = project_journal.id
        if self.type == 'trading' and trading_journal:
            self.journal_id = trading_journal.id
        if self.type == 'maintenance' and  maintenance_journal:
            self.journal_id = maintenance_journal.id

    delivery_note = fields.Char(string='Delivery Note')
    quotation_ref = fields.Char(string='Quotation Ref')
    terms_of_pay = fields.Char(string='Mode/Terms of Payment')
    other_ref = fields.Char(string='Other Reference(s)')
    buyers_order_no = fields.Char(string="Buyer's Order No")
    desp_through = fields.Char(string="Despatched through")
    dest = fields.Char(string="Destination")
    terms_of_del = fields.Char(string="Terms of Delivery")

    @api.onchange('invoicing_percentage')
    def _onchange_invoicing_percentage(self):
        for each in self:
            if each.invoicing_percentage:
                self.percentage_invoiced_amount = (each.amount_total * each.invoicing_percentage) / 100
                if each.line_ids:
                    for each_line in each.line_ids:
                        each_line.invoice_percentage = each.invoicing_percentage
                        each_line.price_unit = each_line.price_unit * (each.invoicing_percentage) / 100

    # def update_analytic_account(self):
    #     AccountMoveLine = self.env['account.move.line']
    #     AnalyticAccount = self.env['account.analytic.account']
    #     Project = self.env['project.project']
    #     project_analytic_account = AnalyticAccount.search([('is_project', '=', True)], limit=1)
    #     trading_analytic_account = AnalyticAccount.search([('is_trading', '=', True)], limit=1)
    #     maintenance_analytic_account = AnalyticAccount.search([('is_maintenance', '=', True)], limit=1)
    #     if not project_analytic_account and not trading_analytic_account and not maintenance_analytic_account:
    #         return
    #     all_lines = AccountMoveLine.sudo().search([('move_id.move_type', 'in', ['out_invoice', 'out_refund'])])
    #     for line in all_lines:
    #         line.analytic_distribution = False
    #         order_id = line.sale_line_ids.mapped('order_id')
    #         project = Project.search([('order_id', '=', order_id.id)], limit=1)
    #         analytic_account_id = project.account_id if project else False
    #         distribution = {}
    #         if analytic_account_id:
    #             distribution[str(analytic_account_id.id)] = 100
    #         if line.move_id.type == 'project' and project_analytic_account:
    #             distribution[str(project_analytic_account.id)] = 100
    #         elif line.move_id.type == 'trading' and trading_analytic_account:
    #             distribution[str(trading_analytic_account.id)] = 100
    #         elif line.move_id.type == 'maintenance' and maintenance_analytic_account:
    #             distribution[str(maintenance_analytic_account.id)] = 100
    #         if distribution:
    #             line.analytic_distribution = distribution
    #         for deferred_line in line.move_id.deferred_move_ids.line_ids:
    #             deferred_move = deferred_line.move_id.deferred_original_move_ids
    #             order_id = deferred_move.line_ids.sale_line_ids.mapped('order_id')
    #             project = Project.search([('order_id', '=', order_id.id)], limit=1)
    #             analytic_account_id = project.account_id if project else False
    #             distribution = {}
    #             if analytic_account_id:
    #                 distribution[str(analytic_account_id.id)] = 100
    #
    #             if deferred_move.type == 'project' and project_analytic_account:
    #                 distribution[str(project_analytic_account.id)] = 100
    #             elif deferred_move.type == 'trading' and trading_analytic_account:
    #                 distribution[str(trading_analytic_account.id)] = 100
    #             elif deferred_move.type == 'maintenance' and maintenance_analytic_account:
    #                 distribution[str(maintenance_analytic_account.id)] = 100
    #
    #             if distribution:
    #                 deferred_line.analytic_distribution = distribution
    #
    #     move_lines = AccountMoveLine.sudo().search(
    #         [('move_id.move_type', 'in', ['entry']), ('analytic_distribution', '=', False),
    #          ('name', 'ilike', 'Deferral of')])
    #     for line in move_lines:
    #         if not line.analytic_distribution and 'Deferral' in (line.name or ''):
    #             text = line.name
    #             parts = text.split(' ')
    #             if len(parts) >= 3:
    #                 ref = parts[-1]
    #             move_id = self.env['account.move'].search([('name', '=', ref)], limit=1)
    #             distribution = {}
    #             if move_id:
    #                 if move_id.type == 'project' and project_analytic_account:
    #                     distribution[str(project_analytic_account.id)] = 100
    #                 elif move_id.type == 'trading' and trading_analytic_account:
    #                     distribution[str(trading_analytic_account.id)] = 100
    #                 elif move_id.type == 'maintenance' and maintenance_analytic_account:
    #                     distribution[str(maintenance_analytic_account.id)] = 100
    #                 if distribution:
    #                     line.analytic_distribution = distribution
    #             else:
    #                 if project_analytic_account:
    #                     distribution[str(project_analytic_account.id)] = 100
    #                 if distribution:
    #                     line.analytic_distribution = distribution



    # def action_update_analytic_account_name(self):
    #     excluded_account_codes = ['251000', '10020201']
    #     for move in self:
    #         for line in move.line_ids:
    #             # Skip accounts that shouldn't have analytic distributions
    #             if line.account_id.code in excluded_account_codes:
    #                 line.analytic_distribution = False
    #                 continue
    #             distribution = line.analytic_distribution
    #             if distribution:
    #                 new_distribution = {}
    #                 updated = False
    #                 for acc_id, percent in distribution.items():
    #                     # Normalize 50% splits to 100%
    #                     if percent == 50:
    #                         new_distribution[acc_id] = 100
    #                         updated = True
    #                     else:
    #                         new_distribution[acc_id] = percent
    #                 if updated:
    #                     line.analytic_distribution = new_distribution
