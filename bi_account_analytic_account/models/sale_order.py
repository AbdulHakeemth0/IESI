from email.policy import default

from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError
from datetime import date
from datetime import datetime,timedelta
# import calendar
from dateutil.relativedelta import relativedelta

from datetime import datetime



class SaleOrder(models.Model):
    _inherit ='sale.order'

    type = fields.Selection([
        ('project', 'Project'),
        ('trading', 'Trading'),
        ('maintenance', 'Maintenance'),
    ], string="Type",default='project')
    next_invoice_date = fields.Date(string="Next Invoice Date")

    def _prepare_invoice(self):
        """Super sale order class and update with fields"""
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'type': self.type,
        })
        return invoice_vals

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)

        for order in self:
            # 1. DEFINE FALLBACKS (Fixes the NameError)
            analytic_account_id = False

            project_id = self.env['project.project'].search(
                [('sale_order_id', '=', order.id)], limit=1
            )
            if project_id:
                analytic_account_id = project_id.account_id

            trading_journal = self.env['account.journal'].sudo().search([('p_t_m_type', '=', 'trading')], limit=1)
            project_journal = self.env['account.journal'].sudo().search([('p_t_m_type', '=', 'project')], limit=1)
            maintenance_journal = self.env['account.journal'].sudo().search([('p_t_m_type', '=', 'maintenance')],
                                                                            limit=1)

            current_datetime = getattr(order, 'next_invoice_date', False) or datetime.now()
            year = str(current_datetime.year)[2:]

            for move in moves.filtered(lambda m: m.invoice_origin == order.name):
                if order.type:
                    move.type = order.type.lower()

                project_analytic = self.env['account.analytic.account'].search([('is_project', '=', True)], limit=1)
                trading_analytic = self.env['account.analytic.account'].search([('is_trading', '=', True)], limit=1)
                maintenance_analytic = self.env['account.analytic.account'].search([('is_maintenance', '=', True)],
                                                                                   limit=1)

                for line in move.line_ids:
                    distribution = {}

                    if analytic_account_id:
                        distribution[str(analytic_account_id.id)] = 100

                    if move.type == 'project' and project_analytic:
                        distribution[str(project_analytic.id)] = 100
                    elif move.type == 'trading' and trading_analytic:
                        distribution[str(trading_analytic.id)] = 100
                    elif move.type == 'maintenance' and maintenance_analytic:
                        distribution[str(maintenance_analytic.id)] = 100

                    if distribution:
                        line.analytic_distribution = distribution

        return moves