{
    'name': 'hms',
    'version': '0.1',
    'depends': ['base', 'crm'],
    'author': 'Ahmed Elsabbagh',
    'category': 'Technical',
    'summary': 'Manage Patients Records',
    'description': 'Module to manage patients in a hospital',
    'data': [
        'security/groups.xml',
        'security/hms_record_rules.xml',
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/dept_views.xml',
        'views/doctor_views.xml',
        'views/partner_views.xml',
        'reports/patient_report_template.xml',
        'reports/patient_report.xml',

    ],
    'installable': True,
    'application': True,
}
