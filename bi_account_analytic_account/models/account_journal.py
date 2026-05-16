from odoo import api, fields, models,_
from datetime import date


class AccountJournal(models.Model):
    _inherit = 'account.journal'



    p_t_m_type = fields.Selection([
        ('project', 'Project'),
        ('trading', 'Trading'),
        ('maintenance', 'Maintenance'),
    ], string="Type(P/T/M)")


# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     module_sale_product_matrix = fields.Boolean("Sale Product Matrix")
#     extract_in_invoice_digitalization_mode = fields.Boolean("Sale Product Matrix")
#     extract_single_line_per_tax = fields.Boolean("Extract Single Line Per Tax")
#     extract_out_invoice_digitalization_mode = fields.Boolean("Extract Out Invoice Digitalization Mode")
#     account_tax_periodicity = fields.Selection([
#         ('monthly', 'Monthly'),
#         ('quarterly', 'Quarterly'),
#         ('yearly', 'Yearly'),
#     ], string="Tax Periodicity")
#
#     account_tax_periodicity_reminder_day = fields.Integer(
#         string="Tax Periodicity Reminder Day",
#         default=1,
#     )
#     account_tax_periodicity_journal_id = fields.Many2one(
#         'account.journal',
#         string='Tax Periodicity Journal',
#     )
#     currency_provider = fields.Selection(
#         [('xe', 'XE'), ('oer', 'Open Exchange Rates'), ('custom', 'Custom')],
#         string="Currency Provider",
#         config_parameter='your_module.currency_provider'
#     )
#     currency_interval_unit = fields.Selection(
#         [
#             ('daily', 'Daily'),
#             ('weekly', 'Weekly'),
#             ('monthly', 'Monthly'),
#             ('yearly', 'Yearly')
#         ],
#         string="Currency Update Interval",
#     )
#     currency_next_execution_date = fields.Date(
#         string="Next Currency Update Date",
#     )
#     totals_below_sections = fields.Boolean(
#         string="Show Totals Below Sections",
#     )
#     account_reports_show_per_company_setting = fields.Boolean(
#         string="Show Account Reports Per Company",
#     )
#
#
# class AccountMove(models.Model):
#     _inherit = 'account.move'
#
#     tax_closing_report_id = fields.Many2one(
#         'account.tax.closing.report',  # Replace with the correct model
#         string="Tax Closing Report"
#     )
#
#     tax_closing_alert = fields.Boolean(
#         string="Tax Closing Alert",
#         default=False
#     )