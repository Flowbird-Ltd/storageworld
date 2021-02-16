# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning


class Crm(models.Model):
    _inherit = "crm.lead"

    number_of_sms = fields.Integer(related="partner_id.number_of_sms")

    def get_messages(self):
        # return window action for the same SMS as partner
        self.ensure_one()
        return self.partner_id.get_messages()
