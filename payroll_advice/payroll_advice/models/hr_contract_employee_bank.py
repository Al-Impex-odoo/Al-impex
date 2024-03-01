from odoo import fields, models, api


class EmployeeBank(models.Model):
    _inherit = 'hr.contract'

    employee_bank_id = fields.Many2one('employee.bank', string='Bank', store=True, traceability='default')
    employee_bank_account = fields.Char(string='Bank Account', store=True, traceability='default')
