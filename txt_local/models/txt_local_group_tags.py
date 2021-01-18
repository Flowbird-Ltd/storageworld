# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests


class TxtLocalGroupTags(models.Model):
    _name = "txt_local.groups.tags"
    _description = "Txt Local Groups Tags"

    name = fields.Char("Name")
