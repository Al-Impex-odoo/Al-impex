{
    'name': 'Payroll Extension',
    'author': 'Natnael Abebaw',
    'description': 'This module contains fields that are not available in the default Odoo payroll system. These fields include allowances, commissions, and deductions, and it also has the capability to calculate employee overtime. Overtime pay is calculated using the following formula: Overtime Pay = Salary / Hourly Salary * (Hours Worked * Factor(1.5, 1.75, 2, 2.5)), This module provides a more detailed and customizable payroll system for businesses with complex compensation structures.',
    'summary': """
                This module contains fields that are not available in the default Odoo payroll system. These fields include allowances and deductions.
                """,
    'version': '0.0.1',
    'category': 'Human Resources/Payroll',
    'depends': ['hr_payroll', 'hr_contract'],
    'data': [
        './views/payroll_extension.xml',
        './views/overtime.xml',
        './views/payroll_loan.xml',
    ],
    'installable': True,
    # 'icon': '',
    'application': False,
    'auto_install': False,
    'sequence': '-1'
}
