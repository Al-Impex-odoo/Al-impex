from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError


class Payroll_Loan(models.Model):
    _inherit = 'hr.contract'

    loan_amount = fields.Monetary(string='Loan Amount', currency_field='currency_id', track_visibility='always',
                                  store=True)
    number_of_months_for_deductions = fields.Float(string='Number of Months for Deductions', digits=(6, 2),
                                                   track_visibility='always',
                                                   onchange="_number_of_months_for_deductions", store=True)
    deduction_start_date = fields.Date(string='Deduction Start Date', track_visibility='always', store=True)
    deduction_end_date = fields.Date(string='Deduction End Date', track_visibility='always', store=True)
    monthly_payment_amount = fields.Monetary(string='Monthly Payment Amount', currency_field='currency_id',
                                             track_visibility='always', compute='_compute_monthly_payment_amount',
                                             store=True)

    @api.depends('loan_amount', 'number_of_months_for_deductions')
    def _compute_monthly_payment_amount(self):
        for record in self:
            if record.loan_amount != 0 and record.number_of_months_for_deductions != 0:
                try:
                    record.monthly_payment_amount = record.loan_amount / record.number_of_months_for_deductions
                except ZeroDivisionError:
                    raise UserError("Please enter start and end date!")

    @api.onchange('deduction_start_date', 'deduction_end_date')
    def _compute_number_of_months_for_deductions(self):
        for record in self:
            if record.deduction_start_date and record.deduction_end_date:
                delta = record.deduction_end_date - record.deduction_start_date
                record.number_of_months_for_deductions = delta.days + 1
                print(datetime.now().date())
            else:
                record.number_of_months_for_deductions = 0
