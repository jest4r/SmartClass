from odoo import models, fields, api

class Students(models.Model):
    _name = "students"
    _description = "Students"
    fullname = fields.Char("fullname", required=True)
    code = fields.Char("Code", required=True)
    dob = fields.Date("Date of Birth", required=True)
    sex = fields.Char("Sex")
    homecity = fields.Char("Home City")
    address = fields.Char("Address")
    hobbies = fields.Char("Hobbies")
    email = fields.Char("Email")
    phone = fields.Char("Phone")
    class_id = fields.Many2one("classes", string="Class")
    facebook = fields.Char("Facebook")
    username = fields.Char("Username", required=True)
    password = fields.Char("Password", required=True)
    description = fields.Text("Description")
    attachment=fields.Char("Attachment")
    haircolor = fields.Char("Hair Color")

