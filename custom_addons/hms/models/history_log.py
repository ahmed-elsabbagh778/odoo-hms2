from odoo import models, fields

class HistoryLog(models.Model):
    _name = "hms.patient.log"

    description = fields.Text()
    patient_id = fields.Many2one('hms.patient')