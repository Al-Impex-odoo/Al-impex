from odoo import fields, models, api
from odoo.exceptions import UserError
from num2words import num2words


class Payroll_Extension(models.Model):
    _inherit = 'hr.contract'

    # Fields defined for allowance
    non_tax_transport_allowance = fields.Monetary(string='Non Taxable Transport Allowance',
                                                  currency_field='currency_id', store=True, track_visibility='always')
    non_tax_transport_allowance_word = fields.Char(string='Non Taxable Transport Allowance In Words', store=True,
                                                   compute="_compute_non_tax_transport_allowance_word")
    wage_word = fields.Char(string='Wage In Words', store=True, compute="_compute_wage_word")
    gross_wage = fields.Monetary(string='Gross Wage', currency_field='currency_id', track_visibility='always',
                                 store=True, compute="_compute_gross_wage")
    gross_wage_word = fields.Char(string='Gross Wage In Words', store=True, compute="_compute_gross_wage_word")
    taxable_transport_allowance = fields.Monetary(string='Taxable Transport Allowance', currency_field='currency_id',
                                                  track_visibility='always', store=True)
    hardship_allowance = fields.Monetary(string='Hardship Allowance', currency_field='currency_id',
                                         track_visibility='always', store=True)
    transport_Per_diem = fields.Monetary(string='Transport Per diem', currency_field='currency_id',
                                         track_visibility='always', store=True)
    per_diem = fields.Monetary(string='Per diem', currency_field='currency_id', track_visibility='always', store=True)
    commission = fields.Monetary(string='Commission', currency_field='currency_id', track_visibility='always',
                                 store=True)

    milk = fields.Monetary(string='Milk', currency_field='currency_id', track_visibility='always', store=True)

    position_allowance = fields.Monetary(string='Position Allowance', currency_field='currency_id',
                                         track_visibility='always', store=True)
    house_allowance = fields.Monetary(string='House Allowance', currency_field='currency_id', track_visibility='always',
                                      store=True)
    reimbursement = fields.Monetary(string='Reimbursement', currency_field='currency_id', track_visibility='always',
                                    store=True)

    # Fields defined for deductions
    food_fee = fields.Monetary(string='Food Fee', currency_field='currency_id', track_visibility='always', store=True)
    other_deduction = fields.Monetary(string='Other Deduction', currency_field='currency_id', track_visibility='always',
                                      store=True)
    absent_deduction = fields.Monetary(string='Absent Deduction', currency_field='currency_id',
                                       track_visibility='always', store=True, compute="_compute_absent_deduction",
                                       readonly=False)
    loan = fields.Monetary(string='Loan', currency_field='currency_id',
                           track_visibility='always', store=True, readonly=True)

    # pension fields
    pension = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Is pension included?', default='no', widget='radio', track_visibility='always')
    pension_11 = fields.Monetary(string='Pension (11%)', currency_field='currency_id', compute='_compute_pension',
                                 store=True)
    pension_7 = fields.Monetary(string='Pension (7%)', currency_field='currency_id', compute='_compute_pension',
                                store=True)

    @api.depends('wage', 'pension')
    def _compute_pension(self):
        for record in self:
            if record.pension == 'yes':
                record.pension_11 = record.wage * 0.11
                record.pension_7 = record.wage * 0.07
            else:
                record.pension_11 = 0.0
                record.pension_7 = 0.0

    @api.depends('wage', 'absent_hours', 'hours_per_week')
    def _compute_absent_deduction(self):
        for record in self:
            try:
                record.absent_deduction = record.wage / (record.hours_per_week * 4) * record.absent_hours
            except ZeroDivisionError:
                raise UserError("Hours per week couldn't be zero!")

    # convert figure to words for
    @api.depends('wage')
    def _compute_wage_word(self):
        for rec in self:
            rec.wage_word = num2words(rec.wage)

    # convert figure to words for non_tax_transport_allowance
    @api.depends('non_tax_transport_allowance')
    def _compute_non_tax_transport_allowance_word(self):
        for rec in self:
            rec.non_tax_transport_allowance_word = num2words(rec.non_tax_transport_allowance)

    # addition of transport allowance and wage
    @api.depends('wage', 'non_tax_transport_allowance')
    def _compute_gross_wage(self):
        for rec in self:
            rec.gross_wage = rec.wage + rec.non_tax_transport_allowance

    # convert figure to words for gross wage
    @api.depends('gross_wage')
    def _compute_gross_wage_word(self):
        for rec in self:
            rec.gross_wage_word = num2words(rec.gross_wage)
