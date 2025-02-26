"""
Project Team Priority Label Model.

This module defines priority labels that can be assigned to projects within teams.
"""

from odoo import models, fields


class ProjectTeamPriorityLabel(models.Model):
    """Team-specific priority labels for projects."""

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
    