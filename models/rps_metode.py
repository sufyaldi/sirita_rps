# -*- coding: utf-8 -*-

from odoo import models, fields

class SiritaRpsMetode(models.Model):
    _name = 'sirita.rps.metode'
    _description = 'Metode Pembelajaran OBE'
    _order = 'id asc'

    name = fields.Char(string='Nama Metode', required=True)
    code = fields.Char(string='Kode/Singkatan', required=True)
    description = fields.Text(string='Deskripsi')
