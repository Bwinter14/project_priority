"""
Project Priority Management Module.

This module implements priority scoring and management for Odoo projects,
including automated calculations and manual overrides.
"""

try:
    from odoo import models, fields, api
    from odoo.exceptions import AccessError
except ImportError:
    # For development environment where Odoo might not be installed
    class models:
        Model = object
    class fields:
        Char = str
        Many2one = object
        Many2many = list
        Float = float
        Integer = int
        Boolean = bool
        Selection = object
        Date = object
    class api:
        @staticmethod
        def depends(*_args):
            """
            Mock implementation of Odoo's @api.depends decorator.
            
            Args:
                *_args: Field names that the computed field depends on
                       (unused in mock implementation)
            
            Returns:
                decorator: A function decorator that simulates @api.depends
            """
            def decorator(func):
                return func
            return decorator
    class AccessError(Exception):
        pass


class ProjectTeam(models.Model):
    _name = 'project.team'
    _description = 'Project Team'
    _inherit = ['mail.thread']

    name = fields.Char(required=True, tracking=True)
    leader_id = fields.Many2one('res.users', string='Team Leader', required=True, tracking=True)
    member_ids = fields.Many2many('res.users', string='Team Members', tracking=True)
    current_capacity = fields.Float(
        string='Current Capacity',
        compute='_compute_current_capacity',
        store=True,
        tracking=True
    )
    capacity_threshold = fields.Float(
        string='Capacity Threshold',
        default=80.0,
        help='Percentage at which capacity warning is triggered',
        tracking=True
    )
    deadline_threshold_days = fields.Integer(
        string='Deadline Warning Threshold',
        default=7,
        help='Days before deadline to show warning',
        tracking=True
    )

    project_ids = fields.One2many('project.project', 'team_id', string='Projects')

    @api.depends('member_ids', 'project_ids')
    def _compute_current_capacity(self):
        for team in self:
            total_capacity = len(team.member_ids) * 100 if team.member_ids else 1
            team.current_capacity = (len(team.project_ids) / total_capacity) * 100


class ProjectTeamPriorityLabel(models.Model):
    _name = 'project.team.priority.label'
    _description = 'Team Priority Label'
    _order = 'sequence'

    name = fields.Char(required=True)
    team_id = fields.Many2one('project.team', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    color = fields.Integer()
    weight = fields.Float(
        default=1.0,
        help='Weight factor for priority calculation'
    )


class ProjectProject(models.Model):
    """
    Extends the project.project model to add priority management features.

    This class adds automated priority scoring based on multiple factors including
    deadlines, inventory impact, and customer urgency. It also supports manual
    priority overrides with appropriate access controls.
    """
    _inherit = 'project.project'
    _description = 'Project with Priority Management'

    priority_score = fields.Float(
        string='Priority Score',
        compute='_compute_priority_score',
        store=True,
        help='Automatically calculated priority score'
    )
    date_deadline = fields.Date(
        string='Deadline',
        tracking=True,
        help='Project completion deadline'
    )
    manual_priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High'),
        ('2', 'Very High'),
        ('3', 'Critical')
    ], string='Manual Priority', default='0', tracking=True)

    deadline_weight = fields.Float(
        string='Deadline Weight',
        default=1.0,
        help='Weight factor for deadline in priority calculation'
    )
    inventory_impact = fields.Selection([
        ('0', 'None'),
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High')
    ], string='Inventory Impact', default='0', tracking=True)

    customer_urgency = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
        ('2', 'Urgent'),
        ('3', 'Critical')
    ], string='Customer Urgency', default='0', tracking=True)

    is_ceo_override = fields.Boolean(
        string='CEO Priority Override',
        default=False,
        tracking=True
    )

    team_id = fields.Many2one(
        'project.team',
        string='Project Team',
        tracking=True
    )

    team_priority_label_id = fields.Many2one(
        'project.team.priority.label',
        string='Team Priority Label',
        domain="[('team_id', '=', team_id)]",
        tracking=True
    )

    team_capacity_warning = fields.Boolean(
        string='Team at Capacity',
        compute='_compute_team_capacity_warning',
        store=True
    )

    dependency_project_ids = fields.Many2many(
        'project.project',
        'project_dependencies_rel',
        'project_id',
        'dependency_id',
        string='Project Dependencies'
    )

    blocked_by_count = fields.Integer(
        string='Blocked By Count',
        compute='_compute_blocked_by_count',
        store=True
    )

    @api.depends('date_deadline', 'inventory_impact', 'customer_urgency', 'manual_priority')
    def _compute_priority_score(self):
        """
        Compute the priority score based on multiple factors.

        The score is calculated using a weighted combination of:
        - Deadline proximity
        - Inventory impact
        - Customer urgency
        - Manual priority settings
        """
        today = fields.Date.today()
        for project in self:
            if project.is_ceo_override:
                project.priority_score = 100.0
                continue

            score = 0.0

            # Deadline weight calculation
            if project.date_deadline:
                days_to_deadline = (project.date_deadline - today).days
                if days_to_deadline <= 0:
                    deadline_score = 100
                elif days_to_deadline <= 7:
                    deadline_score = 75
                elif days_to_deadline <= 30:
                    deadline_score = 50
                else:
                    deadline_score = 25
                score += deadline_score * project.deadline_weight

            # Inventory impact calculation
            inventory_scores = {'0': 0, '1': 25, '2': 50, '3': 75}
            score += inventory_scores.get(project.inventory_impact, 0)

            # Customer urgency calculation
            urgency_scores = {'0': 0, '1': 25, '2': 50, '3': 75}
            score += urgency_scores.get(project.customer_urgency, 0)

            # Manual priority adjustment
            manual_scores = {'0': 0, '1': 25, '2': 50, '3': 75}
            score += manual_scores.get(project.manual_priority, 0)

            project.priority_score = min(score / 4, 100)

    @api.depends('dependency_project_ids')
    def _compute_blocked_by_count(self):
        for project in self:
            project.blocked_by_count = len(project.dependency_project_ids)

    @api.depends('team_id', 'team_id.current_capacity', 'team_id.capacity_threshold')
    def _compute_team_capacity_warning(self):
        for project in self:
            if project.team_id:
                project.team_capacity_warning = (
                    project.team_id.current_capacity >= project.team_id.capacity_threshold
                )
            else:
                project.team_capacity_warning = False

    def action_set_ceo_override(self):
        """
        Set CEO priority override with appropriate access control.

        This method can only be called by users with CEO access rights.
        """
        if not self.env.user.has_group('project_priority.group_project_priority_ceo'):
            raise AccessError("Only CEO can override project priority")
        self.write({'is_ceo_override': True})
        