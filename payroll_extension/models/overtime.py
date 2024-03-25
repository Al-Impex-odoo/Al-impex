from odoo import models, fields, api
from odoo.exceptions import UserError


class PayrollLoan(models.Model):
    _inherit = 'hr.contract'

    absent_hours = fields.Float(string="Absent hours", currency_field='currency_id', track_visibility='always',
                                store=True)
    off_days = fields.Float(string="Off days", track_visibility='always', store=True, compute='_compute_off_days')
    number_of_days = fields.Integer(string="Number of days", track_visibility='always', store=True)

    worked_hour1 = fields.Float(string="Worked hour(1.5)", digits=(6, 2), track_visibility='always')
    worked_hour2 = fields.Float(string="Worked hour(1.75)", digits=(6, 2), track_visibility='always')
    worked_hour3 = fields.Float(string="Worked hour(2)", digits=(6, 2), track_visibility='always')
    worked_hour4 = fields.Float(string="Worked hour(2.5)", digits=(6, 2), track_visibility='always')

    total_overtime = fields.Float(string='Total Overtime', compute='_compute_total_overtime', store=True, readonly=False)

    @api.depends('worked_hour1', 'worked_hour2', 'worked_hour3', 'worked_hour4', 'wage', 'hours_per_week')
    def _compute_total_overtime(self):
        for record in self:
            try:
                total_overtime1 = record.wage / (record.hours_per_week * 4) * (record.worked_hour1 * 1.5)
                total_overtime2 = record.wage / (record.hours_per_week * 4) * (record.worked_hour2 * 1.75)
                total_overtime3 = record.wage / (record.hours_per_week * 4) * (record.worked_hour3 * 2)
                total_overtime4 = record.wage / (record.hours_per_week * 4) * (record.worked_hour4 * 2.5)

                record.total_overtime = total_overtime1 + total_overtime2 + total_overtime3 + total_overtime4
            except ZeroDivisionError:
                raise UserError("Hours per week couldn't be zero!")

    # off days calulation
    @api.depends('number_of_days', 'wage', 'hours_per_week')
    def _compute_off_days(self):
        for record in self:
            record.off_days = record.wage / (record.hours_per_week * 4) * record.number_of_days