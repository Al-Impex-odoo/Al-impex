from datetime import timedelta

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError

class Payroll_Loan(models.Model):
    _inherit = 'hr.contract'

    loan_amount = fields.Monetary(string='Loan Amount', currency_field='currency_id', track_visibility='always',
                                  store=True)
    number_of_months_for_deductions = fields.Float(string='Number of Months for Deductions', digits=(6, 2),
                                                   track_visibility='always', store=True)
    deduction_start_date = fields.Date(string='Deduction Start Date', track_visibility='always', store=True)
    deduction_end_date = fields.Date(string='Deduction End Date', track_visibility='always',
                                     compute="_compute_end_date", store=True)
    monthly_payment_amount = fields.Monetary(string='Monthly Payment Amount', currency_field='currency_id',
                                             track_visibility='always', compute='_compute_monthly_payment_amount',
                                             store=True)

    @api.depends('loan_amount', 'number_of_months_for_deductions')
    def _compute_monthly_payment_amount(self):
        for record in self:
            if record.loan_amount != 0 and record.number_of_months_for_deductions != 0:
                try:
                    record.monthly_payment_amount = record.loan_amount / record.number_of_months_for_deductions
                    record.loan = record.monthly_payment_amount
                except ZeroDivisionError:
                    raise UserError("Please enter start and end date!")

    @api.depends('number_of_months_for_deductions', 'deduction_start_date')
    def _compute_end_date(self):
        for record in self:
            if record.number_of_months_for_deductions and record.deduction_start_date:
                months = int(record.number_of_months_for_deductions)
                start_date = fields.Datetime.from_string(record.deduction_start_date)
                end_date = start_date + relativedelta(months=months) - timedelta(
                    days=1)  # deceases one day from the last month
                record.deduction_end_date = end_date.date()
            else:
                record.deduction_end_date = False
