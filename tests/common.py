"""
Common test utilities and base classes for project_priority tests.

This module provides shared test functionality and setup for all test cases.
"""

from datetime import date, timedelta
from odoo.tests.common import TransactionCase


class TestProjectPriorityCommon(TransactionCase):
    """Base test class for project priority tests."""

    @classmethod
    def setUpClass(cls):  # pylint: disable=invalid-name
        """Set up test data for all test methods."""
        super().setUpClass()

        users = cls.env['res.users'].with_context(
            no_reset_password=True,
            mail_create_nosubscribe=True
        )

        cls.user = users.create({
            'name': 'Base User',
            'login': 'base_user',
            'email': 'base@example.com',
            'groups_id': [(4, cls.env.ref('project_priority.group_project_priority_user').id)]
        })

        cls.manager = users.create({
            'name': 'Project Manager',
            'login': 'project_manager',
            'email': 'manager@example.com',
            'groups_id': [(4, cls.env.ref('project_priority.group_project_priority_manager').id)]
        })

        cls.ceo = users.create({
            'name': 'Company CEO',
            'login': 'company_ceo',
            'email': 'ceo@example.com',
            'groups_id': [(4, cls.env.ref('project_priority.group_project_priority_ceo').id)]
        })

        cls.team = cls.env['project.team'].create({
            'name': 'Base Team',
            'leader_id': cls.manager.id,
            'member_ids': [(4, cls.user.id)],
            'capacity_threshold': 80.0,
            'deadline_threshold_days': 7
        })

        cls.priority_labels = cls.env['project.team.priority.label'].create([
            {
                'name': 'Low',
                'team_id': cls.team.id,
                'sequence': 10,
                'weight': 0.5
            },
            {
                'name': 'Medium',
                'team_id': cls.team.id,
                'sequence': 20,
                'weight': 1.0
            },
            {
                'name': 'High',
                'team_id': cls.team.id,
                'sequence': 30,
                'weight': 2.0
            }
        ])

        cls.project = cls.env['project.project'].create({
            'name': 'Base Project',
            'team_id': cls.team.id,
            'manual_priority': '1',
            'inventory_impact': '1',
            'customer_urgency': '1',
            'date_deadline': date.today() + timedelta(days=30),
            'team_priority_label_id': cls.priority_labels[1].id  # Medium priority
        })

    def setUp(self):  # pylint: disable=invalid-name
        """Reset test data before each test method."""
        super().setUp()
        self.project.write({
            'is_ceo_override': False,
            'manual_priority': '1'
        })
        