from odoo import fields, models, api

class Payroll_Extension(models.Model):
    _inherit = 'hr.contract'

    # Fields defined for allowance
    non_tax_transport_allowance = fields.Monetary(string='Non Taxable Transport Allowance', currency_field='currency_id', track_visibility='always')
    taxable_transport_allowance = fields.Monetary(string='Taxable Transport Allowance', currency_field='currency_id', track_visibility='always')
    transport_Per_diem = fields.Monetary(string='Transport Per diem', currency_field='currency_id', track_visibility='always')
    per_diem = fields.Monetary(string='Per diem', currency_field='currency_id', track_visibility='always')
    commission = fields.Monetary(string='Commission', currency_field='currency_id', track_visibility='always')
    hardship_allowance = fields.Monetary(string='Hardship Allowance', currency_field='currency_id', track_visibility='always')
    milk = fields.Monetary(string='Milk', currency_field='currency_id', track_visibility='always')

    #fields for allowance only in Al-impex business plc
    position_allowance = fields.Monetary(string='Position Allowance', currency_field='currency_id', track_visibility='always')
    house_allowance = fields.Monetary(string='House Allowance', currency_field='currency_id', track_visibility='always')

    # Fields defined for deductions
    food_fee = fields.Monetary(string='Food Fee', currency_field='currency_id', track_visibility='always')
    other_deduction = fields.Monetary(string='Other Deduction', currency_field='currency_id', track_visibility='always')

    # fields for allowance only in Al-impex business plc
    loan = fields.Monetary(string='Loan', currency_field='currency_id', track_visibility='always')
    reimbursement = fields.Monetary(string='Reimbursement', currency_field='currency_id', track_visibility='always')

    #pension fields
    pension = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Is pension included?', default='no', widget='radio', track_visibility='always')
    pension_11 = fields.Monetary(string='Pension (11%)', currency_field='currency_id', compute='_compute_pension')
    pension_7 = fields.Monetary(string='Pension (7%)', currency_field='currency_id', compute='_compute_pension')

    @api.depends('wage', 'pension')
    def _compute_pension(self):
        for record in self:
            if record.pension == 'yes':
                record.pension_11 = record.wage * 0.11
                record.pension_7 = record.wage * 0.07
            else:
                record.pension_11 = 0.0
                record.pension_7 = 0.0
