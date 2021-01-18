# -*- coding: utf-8 -*-

import requests
import json
from odoo import _
from odoo.exceptions import Warning


# ERROR CODES https://api.txtlocal.com/docs/sendsms
SEND_ERROR_CODES = {
    "1": "No command specified",
    "2": "Unrecognised command",
    "3": "Invalid login details",
    "4": "No recipients specified",
    "5": "No message content",
    "6": "Message too long",
    "7": "Insufficient credits",
    "8": "Invalid schedule date",
    "9": "Schedule date is in the past",
    "10": "Invalid group ID",
    "11": "Selected group is empty",
    "32": "Invalid number format",
    "33": "You have supplied too many numbers",
    "34": "You have supplied both a group ID and a set of numbers",
    "43": "Invalid sender name",
    "44": "No sender name specified",
    "51": "No valid numbers specified"
}


class TxtLocal:

    def send_txt_message(self, env_obj, data):
        # add extra fields to data that are from settings file
        api_key = env_obj.env["ir.config_parameter"].sudo().get_param("txt_local.txt_local_api_key")
        test = env_obj.env["ir.config_parameter"].sudo().get_param("txt_local.txt_local_test_api")
        if api_key:
            data["api_key"] = api_key

            if test:
                data["test"] = "true"  # Remove on production

            response = requests.post("https://api.txtlocal.com/send/", params=data)
            response.raise_for_status()
            response = response.json()

            # check for errors
            if response.get("status") == "success":
                return response
            else:
                # check error code in array
                error_message = SEND_ERROR_CODES.get(response.get("errors").get("code"))
                if error_message:
                    raise Warning(_(error_message))
                else:
                    raise Warning(_("Unknown API Error Occurred"))
        else:
            raise Warning(_("Please input your API Key in the settings page before sending SMS messages"))
