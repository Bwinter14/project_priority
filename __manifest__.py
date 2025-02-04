{
    'name': 'Project Priority',
    'version': '18.0.1.0.0',
    'category': 'Project',
    'summary': 'Automated project prioritization with manual override capabilities',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'AGPL-3',
    'depends': ['project', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/project_priority_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}