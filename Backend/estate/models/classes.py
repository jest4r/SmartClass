from odoo import models, fields, api

class Classes(models.Model):
    _name="classes"
    _description="Classes"
    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    code = fields.Char("Code", required=True)