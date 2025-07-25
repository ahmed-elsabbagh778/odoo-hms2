from odoo import models, fields

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Hospital Department'

    name = fields.Char(required=True)
    capacity = fields.Integer()
    is_openned = fields.Boolean()
    patient_ids = fields.One2many('hms.patient', 'department_id', string="Patients")
