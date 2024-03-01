from odoo import fields, models, api
from datetime import datetime
from num2words import num2words


class PayslipInfo(models.Model):
    _inherit = 'hr.payslip'

    employee_bank = fields.Many2one(related='contract_id.employee_bank_id', string="Bank", store=True)
    employee_bank_account = fields.Char(related='contract_id.employee_bank_account', string="Bank Account", store=True)

    month_year = fields.Char(string='month_year')
    formatted_date_from = fields.Char(string='Formatted Date', compute='_compute_formatted_date')

    total_net_wage_in_words = fields.Char(string='Number in Words', )
    total_net_wage = fields.Float(string='Total Wages', )
    selected_record_wage = 0

    @api.depends('date_from')
    def _compute_formatted_date(self):
        # change date format from 02/03/2023 to March 02/2023
        for rec in self:
            if rec.date_from:
                date = fields.Date.from_string(rec.date_from)
                rec.formatted_date_from = date.strftime('%B %d/%Y')
                rec.month_year = rec.date_from.strftime('%B %Y')
            else:
                rec.formatted_date_from = False

    def get_selected_record(self):
        # get selected record wage in tree view
        selected_records = self.env['hr.payslip'].browse(self.env.context.get('active_ids'))
        selected_record_wage = selected_records.mapped('net_wage')
        total = sum(selected_record_wage)

        self.total_net_wage = total
        self.compute_figure_to_words(total)

    def compute_figure_to_words(self, number):
        # change number in words from 101.23 to one hundred and one point two three
        self.total_net_wage_in_words = num2words(number)
        print("number in words: ", self.total_net_wage_in_words)
        print(number)

    def action_print_bank_advice(self):
        for rec in self:
            rec.get_selected_record()
        return self.env.ref('payroll_advice.action_report_payroll_bank_advice').report_action(self)