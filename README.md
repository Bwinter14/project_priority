# Project Priority Module for Odoo 18

## Project Structure
```
project_priority/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── project_priority.py
│   └── project_team.py
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── static/
│   └── description/
│       ├── icon.png
│       └── index.html
├── tests/
│   ├── __init__.py
│   ├── common.py
│   ├── test_project_priority.py
│   └── test_project_team.py
├── views/
│   └── project_priority_views.xml
├── requirements.txt
└── requirements-dev.txt
```

## Development Setup

1. **System Requirements**
   - Python 3.10+
   - PostgreSQL 15+
   - Node.js 18+
   - Git

2. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Development Tools**
   - Flake8: Code style guide enforcement
   - Pylint: Python code analysis
   - Black: Code formatting
   - Bandit: Security linting
   - Safety: Dependency security checks

## Testing

1. **Test Environment Setup**
   ```bash
   createdb odoo_test
   odoo -d odoo_test -i project_priority --test-enable --stop-after-init
   ```

2. **Running Tests**
   ```bash
   pytest tests/
   ```

3. **Code Quality Checks**
   ```bash
   flake8 .
   pylint **/*.py
   black .
   bandit -r .
   safety check
   ```

## CI/CD Pipeline

The module includes a GitHub Actions workflow that:
1. Runs linting checks
2. Executes unit tests
3. Performs security scanning
4. Creates releases for tagged versions

## Module Features

1. **Project Priority Management**
   - Automated priority calculation
   - Manual priority override
   - CEO priority override capability
   - Priority-based sorting and filtering

2. **Team Management**
   - Team capacity tracking
   - Resource allocation
   - Workload management
   - Custom priority labels

3. **Security**
   - Role-based access control
   - Three-tier permission system:
     - Users: View access
     - Managers: Edit access
     - CEO: Full access with override capabilities

## Best Practices

1. **Code Quality**
   - Follow [OCA Guidelines](https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst)
   - Use type hints where possible
   - Write comprehensive docstrings
   - Keep methods focused and small

2. **Testing**
   - Write tests for all new features
   - Maintain test coverage above 80%
   - Use appropriate test decorators
   - Mock external dependencies

3. **Security**
   - Implement proper access controls
   - Validate all user inputs
   - Use secure default values
   - Regular dependency updates

4. **Performance**
   - Optimize database queries
   - Use appropriate indexes
   - Implement caching where beneficial
   - Monitor resource usage

## Common Issues and Solutions

1. **Installation**
   - Ensure all dependencies are installed
   - Check PostgreSQL connection
   - Verify Odoo version compatibility
   - Clear browser cache after updates

2. **Testing**
   - Use correct test database
   - Reset test data between runs
   - Mock external services
   - Handle transaction rollbacks

3. **Security**
   - Review access rights regularly
   - Test with different user roles
   - Validate data access patterns
   - Monitor security advisories

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

This module is licensed under the AGPL-3 License.