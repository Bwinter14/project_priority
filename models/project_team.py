"""
Project Team Management Module.

This module implements team management functionality including capacity tracking
and resource allocation.
"""

from odoo import models, fields, api


class ProjectTeam(models.Model):
    """Project team model for managing team resources and capacity."""

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
        """Calculate current team capacity based on team members and projects."""
        for team in self:
            total_capacity = len(team.member_ids) * 100 if team.member_ids else 1
            team.current_capacity = (len(team.project_ids) / total_capacity) * 100
            