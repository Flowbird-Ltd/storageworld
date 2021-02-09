# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from .txt_local import TxtLocal
import requests
import json


class TxtLocalMessages(models.Model):
    _name = 'txt_local.messages'
    _description = 'Txt Local Messages'
    _order = "create_date desc"

    name = fields.Char("Name")
    sender = fields.Char("Sender")
    default_sender = fields.Boolean("Default Sender", default=True, help="Enable Replies")
    message = fields.Char("Message")
    contact_ids = fields.Many2many("res.partner", string="Related Contacts")
    numbers = fields.Char("Number", compute="_compute_mobile_number", required=True)
    inbound_outbound = fields.Selection([
        ("inbound", "Inbound"),
        ("outbound", "Outbound")
    ], default="outbound")
    status = fields.Selection([
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("failed", "Failed")
    ])
    failure_reason = fields.Char("Failure Reason")  # only visible when error occurred
    read_status = fields.Boolean("Read Status")

    # add note to the chatter on the contact level
    def add_note_to_chatter_contact(self, result):
        for contact in result.contact_ids:
            self.env["mail.message"].create(
                [
                    {
                        "message_type": "sms",
                        "body": "SMS: " + result.message,
                        "res_id": contact.id,
                        "model": "res.partner",
                        "subtype_id": "2"
                    }
                ]
            )

    # use the TxtLocal object to send the SMS text
    def send_txt_message(self):
        txt_local_instance = TxtLocal()

        for record in self:
            data = {
                "message": record.message,
                "numbers": record.numbers
            }

            if not record.default_sender:
                data["sender"] = record.sender
            else:
                # get the default number from the settings and set as sender
                default_number = self.env["ir.config_parameter"].sudo().get_param("txt_local.txt_local_default_number")

                if default_number:
                    data["sender"] = default_number
                else:
                    raise Warning(_("No default number has been set"))

            txt_local_instance.send_txt_message(self, data)
            return True

    # auto compute the numbers from all the contacts
    @api.depends("contact_ids")
    def _compute_mobile_number(self):
        for record in self:
            numbers = ""
            if record.contact_ids:
                for contact in record.contact_ids:
                    if contact.mobile or contact.phone:
                        numbers += contact.mobile + "," if contact.mobile else contact.phone + ","
            # remove the last comma
            record.numbers = numbers[:-1]

    # send the sms message when the record is created and outbound
    @api.model
    def create(self, vals):
        result = super(TxtLocalMessages, self).create(vals)

        # add the sequence to the name of the record
        sequence_number = self.env["ir.sequence"].get("txt_local.messages")
        result.name = sequence_number

        # send message, if outbound, when saved and add sent result
        if result.inbound_outbound == "outbound" and result.status != "sent":
            sent = result.send_txt_message()
            if sent:
                result.status = "sent"

        # create note on chatter
        self.add_note_to_chatter_contact(result)

        return result
