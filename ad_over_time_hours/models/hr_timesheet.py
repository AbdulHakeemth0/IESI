from odoo import models, fields, api, _

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    ot_hours = fields.Float(
        string="OT Hours",
        compute="_compute_ot_hours",
        store=True
    )
    taxi_amount = fields.Monetary(string="Taxi Amount")
    department_id = fields.Many2one(
        'hr.department',
        string="Department",
        related='employee_id.department_id',
        store=True,
        readonly=True
    )


    @api.depends('unit_amount', 'employee_id', 'date')
    def _compute_ot_hours(self):
        for rec in self:
            rec.ot_hours = 0.0  # default
            if not rec.employee_id or not rec.date:
                continue
            contract = rec.employee_id.contract_id
            if not contract or not contract.daily_working_hours:
                continue
            same_day_lines = self.search([
                ('employee_id', '=', rec.employee_id.id),
                ('date', '=', rec.date),
            ])

            total_hours = sum(line.unit_amount or 0.0 for line in same_day_lines)
            if total_hours > contract.daily_working_hours:
                total_ot = total_hours - contract.daily_working_hours
                if rec.id == same_day_lines.sorted('id')[-1].id:
                    rec.ot_hours = total_ot
                else:
                    rec.ot_hours = 0.0
            else:
                rec.ot_hours = 0.0


    # @api.depends('unit_amount', 'employee_id')
    # def _compute_ot_hours(self):
    #     for rec in self:
    #         ot = 0.0
    #
    #         if rec.employee_id and rec.unit_amount:
    #             # Get active contract of employee
    #             contract = rec.employee_id.contract_id
    #
    #             if contract and contract.daily_working_hours:
    #                 if rec.unit_amount > contract.daily_working_hours:
    #                     ot = rec.unit_amount - contract.daily_working_hours
    #
    #         rec.ot_hours = ot
