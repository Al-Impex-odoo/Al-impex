from odoo import fields, models, api


class EmployeeBank(models.Model):
    _name = 'employee.bank'
    _description = 'Employee Bank'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Bank Name', required=True)
    bank_account = fields.Char(string='Bank Account', required=True)
    bank_branch = fields.Char(string='Bank Branch', required=True)
    bank_state_id = fields.Many2one('res.country.state', string='State', required=True, store=True)
    bank_country_id = fields.Many2one('res.country', string='Country', required=True, )
    # advice_signer_id = fields.Many2many('hr.employee', string='Advice Signer', required=True, store=True)

    @api.depends('name', 'bank_account')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = '%s (%s)' % (rec.name, rec.bank_account)