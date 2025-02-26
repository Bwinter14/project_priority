"""
Common test mocks for Odoo modules.
"""

from unittest.mock import MagicMock, patch
import pytest

# Mock the odoo module
odoo_mock = MagicMock()
models_mock = MagicMock()
fields_mock = MagicMock()
api_mock = MagicMock()


@pytest.fixture(autouse=True)
def mock_odoo():
    """Mock odoo and its submodules."""
    with patch.dict('sys.modules', {
        'odoo': odoo_mock,
        'odoo.models': models_mock,
        'odoo.fields': fields_mock,
        'odoo.api': api_mock,
        'odoo.exceptions': MagicMock(),
        'odoo.tests': MagicMock(),
        'odoo.tests.common': MagicMock()
    }):
        yield


@pytest.fixture
def mock_environment():
    """Create a mock environment for testing."""
    env = MagicMock()

    # Mock users
    user = MagicMock(id=1, name='Base User')
    manager = MagicMock(id=2, name='Project Manager')
    ceo = MagicMock(id=3, name='Company CEO')

    env.ref.side_effect = lambda x: {
        'project_priority.group_project_priority_user': MagicMock(id=1),
        'project_priority.group_project_priority_manager': MagicMock(id=2),
        'project_priority.group_project_priority_ceo': MagicMock(id=3)
    }.get(x, MagicMock())

    env['res.users'].create.side_effect = [user, manager, ceo]
    env['project.project'].new = MagicMock(return_value=MagicMock())
    env['project.team'].new = MagicMock(return_value=MagicMock())

    return env
