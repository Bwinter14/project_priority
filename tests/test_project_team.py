"""
Test cases for project team functionality.
"""

from .test_mocks import mock_odoo  # pylint: disable=unused-import


def test_team_capacity(mock_environment):
    """Test team capacity calculation."""
    # Create test team
    team = mock_environment['project.team'].new()
    team.name = 'Test Team'
    team.leader_id = mock_environment['res.users'].browse(2)
    team.member_ids = mock_environment['res.users'].browse([1])
    team.capacity_threshold = 80.0
    team.current_capacity = 50.0

    initial_capacity = team.current_capacity

    # Simulate adding projects
    team.project_ids = [team.env['project.project'].new() for _ in range(3)]
    team.compute_current_capacity()

    assert team.current_capacity > initial_capacity


def test_team_member_management(mock_environment):
    """Test team member management."""
    # Create test team
    team = mock_environment['project.team'].new()
    team.name = 'Test Team'
    team.leader_id = mock_environment['res.users'].browse(2)
    team.member_ids = mock_environment['res.users'].browse([1])

    new_member = mock_environment['res.users'].new({
        'id': 3,
        'name': 'New Member'
    })

    # Add new member
    team.write({'member_ids': [(4, new_member.id)]})
    assert new_member in team.member_ids

    # Change team leader
    team.write({'leader_id': new_member.id})
    assert team.leader_id == new_member