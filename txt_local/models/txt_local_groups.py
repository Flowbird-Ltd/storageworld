# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from .txt_local import TxtLocal

class TxtLocalGroups(models.Model):
    _name = 'txt_local.groups'
    _inherit = "mail.thread"
    _description = 'Txt Local Groups'

    name = fields.Char("Group Name")
    tags = fields.Many2many("txt_local.groups.tags", string="Tags")
    contact_ids = fields.Many2many("res.partner", string="Contacts")

    def send_message(self):
        # if the all the contacts have either a phone number or mobile
        all_contacts = True
        for contact in self.contact_ids:
            if contact.mobile is False and contact.phone is False:
                all_contacts = False

        if all_contacts:
            # open view which creates a new message
            view_id = self.env.ref("txt_local.pop_up_send_message").id
            return{
                "type": "ir.actions.act_window",
                "res_model": "txt_local.messages",
                "views": [(view_id, "form")],
                "target": "new",
                "context": {
                    "default_contact_ids": self.contact_ids.ids,
                    "default_inbound_outbound": "outbound"
                }
            }
        else:
            raise Warning(_("All contacts needs a mobile or phone number"))
