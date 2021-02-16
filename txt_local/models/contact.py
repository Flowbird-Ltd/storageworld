# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning
import requests


class Contact(models.Model):
    _inherit = "res.partner"

    number_of_sms = fields.Integer(compute="_compute_number_of_sms")

    def _compute_number_of_sms(self):
        for record in self:
            record.number_of_sms = self.env["txt_local.messages"].search_count([("contact_ids", "in", record.id)])

    def get_messages(self):
        # return window action for the same SMS
        self.ensure_one()

        tree_view = self.env.ref("txt_local.messages_main_list").id
        form_view = self.env.ref("txt_local.messages_form").id
        # return a window action which will display all SMS's relating to contact

        return {
            "type": "ir.actions.act_window",
            "name": "SMS",
            "views": [(tree_view, "tree"), (form_view, "form")],
            "res_model": "txt_local.messages",
            "domain": [("contact_ids", "in", self.id)],
            "context": "{'create': False}"
        }

    def send_message(self):
        # if the contact has a phone/mobile number
        if self.phone or self.mobile:
            # open view which creates a new message
            view_id = self.env.ref("txt_local.pop_up_send_message").id
            return {
                "type": "ir.actions.act_window",
                "res_model": "txt_local.messages",
                "views": [(view_id, "form")],
                "target": "new",
                "context": {
                    "default_contact_ids": [self.id],
                    "default_inbound_outbound": "outbound"
                }
            }
        else:
            raise Warning(_("The Contact needs a mobile or phone number"))

    # remove blank spaces from phone to enable search
    @api.onchange("phone")
    def remove_spaces_from_phone(self):
        for record in self:
            if record.phone:
                record.phone = record.phone.replace(" ", "")

    # remove black spaces from mobile to enable search
    @api.onchange("mobile")
    def remove_spaces_from_mobile(self):
        for record in self:
            if record.mobile:
                record.mobile = record.mobile.replace(" ", "")
