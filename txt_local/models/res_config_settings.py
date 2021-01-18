# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TxtLocalSettings(models.TransientModel):
    _inherit = "res.config.settings"

    txt_local_api_key = fields.Char("API Key", config_parameter="txt_local.txt_local_api_key")
    txt_local_test_api = fields.Boolean("Test API", config_parameter="txt_local.txt_local_test_api")
