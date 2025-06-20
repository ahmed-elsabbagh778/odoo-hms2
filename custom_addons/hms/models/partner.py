from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")
    vat = fields.Char(string="Tax ID", required=True)

    @api.constrains('related_patient_id')
    def _check_unique_patient_email(self):
        for rec in self:
            patient = rec.related_patient_id
            if patient and patient.email:
                existing_partners = self.env['res.partner'].search([
                    ('id', '!=', rec.id),
                    ('related_patient_id.email', '=', patient.email)
                ])
                if existing_partners:
                    raise ValidationError(
                        f"This patient ({patient.first_name} {patient.last_name}) is already linked to another customer with the same email: {patient.email}."
                    )

    _sql_constraints = [
        ('unique_email', 'unique(email)', 'Email must be unique!')
    ]

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError(f"Cannot delete customer '{rec.name}' because they are linked to a patient.")
        return super().unlink()
