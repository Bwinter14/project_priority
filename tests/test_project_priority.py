"""
Test cases for project priority functionality.
"""

from datetime import date, timedelta
import pytest
from .test_mocks import mock_odoo  # pylint: disable=unused-import


def test_priority_score_calculation(mock_environment):
    """Test priority score calculation."""
    # Create test project
    project = mock_environment['project.project'].new()
    project.priority_score = 50.0
    project.manual_priority = '1'
    project.inventory_impact = '1'
    project.customer_urgency = '1'
    project.date_deadline = date.today() + timedelta(days=30)

    # Test normal priority
    project.compute_priority_score()
    assert 0 <= project.priority_score <= 100

    # Test high priority
    project.manual_priority = '3'
    project.inventory_impact = '3'
    project.customer_urgency = '3'
    project.compute_priority_score()
    assert project.priority_score > 75


def test_access_rights(mock_environment):
    """Test access rights for different user levels."""
    # Create test project
    project = mock_environment['project.project'].new()
    project.priority_score = 50.0

    # Test user access (should raise AccessError)
    with pytest.raises(Exception):
        project.with_user(mock_environment['res.users'].browse(1)).write({'manual_priority': '2'})

    # Test manager access (should succeed)
    project.with_user(mock_environment['res.users'].browse(2)).write({'manual_priority': '2'})

    # Test CEO access (should succeed and allow override)
    project.with_user(mock_environment['res.users'].browse(3)).write({
        'is_ceo_override': True,
        'manual_priority': '3'
    })