{
        'name': 'Payroll Advice',
        'author': 'Natnael Abebaw',
        'description': '',
        'summary': """
                    
                    """,
        'version': '0.0.1',
        'category': 'Human Resources/Payroll',
        'depends': ['base','hr_payroll', 'hr_contract', 'hr', 'base'],
        'data': [
                'security/ir.model.access.csv',
                'views/hr_contract_employee_bank_view.xml',
                'views/hr_employee_bank_view.xml',
                'views/payslip_info_view.xml',
                'report/payroll_bank_advice_templates.xml',
        ],
        'installable': True,
        # 'icon': '',
        'application': False,
        'auto_install': False,
        'sequence': '-1'
    }
