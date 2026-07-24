# -*- coding: utf-8 -*-

from odoo import models, fields

class SiritaRpsKurikulum(models.Model):
    _name = 'sirita.rps.kurikulum'
    _description = 'Kurikulum'
    _order = 'name desc'

    name = fields.Char(string='Nama Kurikulum', required=True)
