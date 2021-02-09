# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.http import Response


class TxtLocalInbound(http.Controller):
    # set <url>/txt_local/inbound_message/ as forward route on inboxes
    @http.route("/txt_local/inbound_message/", auth="public", type="http", csrf=False)
    def message_received(self, **kw):
        # Message Data
        data = request.params
        in_number = data["sender"]

        # remove 44 / 07 and check if ilike rather than equal
        in_number = in_number[2:]

        # search for a contact where in_number = phone or mobile
        contacts = request.env["res.partner"].sudo().search(
            [
                "|",
                ("phone", "ilike", in_number),
                ("mobile", "ilike", in_number)
            ]
        )

        # based on search create the messages
        for contact in contacts:
            request.env["txt_local.messages"].sudo().create(
                [
                    {
                        "contact_ids": [(4, contact.id, 0)],
                        "sender": data["sender"],
                        "message": data["content"],
                        "inbound_outbound": "inbound",
                        "read_status": False
                    }
                ]
            )

        return Response(status=200)
