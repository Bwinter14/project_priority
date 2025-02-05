from odoo import models, fields  # noqa: E0401


class ProjectProject(models.Model):

    _inherit = 'project.project'

    priority_score = fields.Float(
        string='Priority Score',
        compute='_compute_priority_score',
        store=True,
        help='Automatically calculated priority score'
    )

    manual_priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High'),
        ('2', 'Very High'),
        ('3', 'Critical')
    ], string="Manual Priority")

# Ensure a newline at the end of the file
