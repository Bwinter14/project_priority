# Project Priority Module API Documentation

## Models

### project.project

Extended model for project management with priority features.

#### Fields

| Field Name | Type | Description |
|------------|------|-------------|
| priority_score | Float | Automatically calculated priority score (0-100) |
| manual_priority | Selection | Manual priority setting (Normal/High/Very High/Critical) |
| inventory_impact | Selection | Impact on inventory (None/Low/Medium/High) |
| customer_urgency | Selection | Customer urgency level (Normal/Important/Urgent/Critical) |
| is_ceo_override | Boolean | CEO priority override flag |
| team_id | Many2one | Link to project team |
| team_priority_label_id | Many2one | Team-specific priority label |
| dependency_project_ids | Many2many | Related project dependencies |

#### Methods

```python
def _compute_priority_score(self):
    """Compute the priority score based on multiple factors."""
    
def action_set_ceo_override(self):
    """Set CEO priority override with appropriate access control."""
```

### project.team

Model for managing project teams and workload.

#### Fields

| Field Name | Type | Description |
|------------|------|-------------|
| name | Char | Team name |
| leader_id | Many2one | Team leader |
| member_ids | Many2many | Team members |
| current_capacity | Float | Current team capacity percentage |
| capacity_threshold | Float | Capacity warning threshold |
| deadline_threshold_days | Integer | Days before deadline for warning |

#### Methods

```python
def _compute_current_capacity(self):
    """Calculate current team capacity based on projects and members."""
```

## Security Groups

1. `group_project_priority_user`
   - Basic access to view priorities and teams
   
2. `group_project_priority_manager`
   - Can modify priorities and manage teams
   
3. `group_project_priority_ceo`
   - Full access with override capabilities

## Record Rules

Detailed access control rules for each model and user group.

## Usage Examples

```python
# Calculate priority score
project = env['project.project'].browse(project_id)
project._compute_priority_score()

# Set CEO override
if env.user.has_group('project_priority.group_project_priority_ceo'):
    project.action_set_ceo_override()

# Check team capacity
team = env['project.team'].browse(team_id)
team._compute_current_capacity()
```