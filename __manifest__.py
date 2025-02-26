{
    'name': 'Project Priority',
    'version': '18.0.1.0.0',
    'category': 'Project',
    'summary': 'Automated project prioritization with manual override capabilities',
    'author': '3C LLC',
    'website': 'https://www.3clabsllc.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'web',
        'mail',
        'project',
        'hr',
        'contacts',
        'stock',
        'resource',
        'board'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/project_priority_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
    'description': """
Project Priority Management
==========================

This module adds automated priority scoring and management capabilities to Odoo projects:

* Automated priority calculation based on multiple factors
* Manual priority override with access controls
* CEO priority override capability
* Priority-based project sorting and filtering
* Team workload management
* Custom priority labels
* Resource allocation and tracking
* Team capacity management
* Inventory impact assessment
* HR integration for team management
""",
}