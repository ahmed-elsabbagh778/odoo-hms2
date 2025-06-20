from odoo import models, fields, api

class Doctor(models.Model):
    _name = 'hms.doctors'
    _description = 'Hospital Doctors'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Image()
    patient_ids = fields.Many2many('hms.patient', string="Patients")

    name = fields.Char(compute="_compute_name", store=True)

    @api.depends("first_name", "last_name")
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.first_name or ''} {rec.last_name or ''}".strip()
