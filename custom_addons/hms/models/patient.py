from stdnum.exceptions import ValidationError

from odoo import models, fields, api
import re

from odoo.tools import unique

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    first_name = fields.Char()
    last_name = fields.Char()
    email = fields.Char(string="Email", required=True, unique=True)
    birth_date = fields.Date()
    history = fields.Text()
    cr_ratio = fields.Float(string='CR RATIO')
    blood_type = fields.Selection(
        [
            ('a', 'A'),
            ('b', 'B'),
            ('ab', 'AB'),
            ('o', 'O')
        ], string="Blood Type"
    )
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer(compute="_compute_age", store=True)
    department_id = fields.Many2one('hms.department', string="Department")
    doctor_ids = fields.Many2many('hms.doctors', string="Doctors")
    require_cr_ratio = fields.Boolean(compute='_compute_require_cr_ratio')
    doctor_readonly = fields.Boolean(compute='_compute_doctor_readonly')
    history_readonly = fields.Boolean(compute='_compute_history_readonly')

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')

    state_logs = fields.One2many('hms.patient.log', 'patient_id')

    @api.onchange('pcr')
    def _onchange_pcr(self):
        if self.pcr:
            self.cr_ratio = 0.0

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_required(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked.")

    @api.constrains('department_id')
    def _check_department_open(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_openned:
                raise ValidationError("You can't assign a closed department.")

    @api.depends('pcr')
    def _compute_require_cr_ratio(self):
        for rec in self:
            rec.require_cr_ratio = rec.pcr

    @api.depends('department_id')
    def _compute_doctor_readonly(self):
        for rec in self:
            rec.doctor_readonly = not bool(rec.department_id)

    @api.depends("birth_date")
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = fields.Date.today()
                rec.age = today.year - rec.birth_date.year - (
                        (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0

    @api.onchange("age")
    def _onchange_age_set_pcr(self):
        for rec in self:
            if rec.age and rec.age < 30 and not rec.pcr:
                rec.pcr = True
                return {
                    "warning": {
                        "title": "PCR Automatically Checked",
                        "message": "PCR field has been checked automatically because the patient is under 30.",
                        "type": "notification"
                    }
                }

    @api.depends('age')
    def _compute_history_readonly(self):
        for rec in self:
            rec.history_readonly = rec.age < 50

    def create_state_log(self):
        vals = {
            'description': 'state Changed to %s' % (self.state),
            'patient_id': self.id
        }
        self.env['hms.patient.log'].create(vals)

    def write(self, vals):
        res = super(Patient, self).write(vals)
        if 'state' in vals:
            for rec in self:
                rec.create_state_log()
        return res

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if not rec.email or not re.match(EMAIL_REGEX, rec.email):
                raise ValidationError("Please enter a valid email address.")

            domain = [('email', '=', rec.email)]
            if rec.id:
                domain.append(('id', '!=', rec.id))
            existing = self.search(domain, limit=1)
            if existing:
                raise ValidationError("Email must be unique. This email is already used.")


