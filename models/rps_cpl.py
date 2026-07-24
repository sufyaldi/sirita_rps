# -*- coding: utf-8 -*-

from odoo import models, fields

class SiritaRpsCpl(models.Model):
    _name = 'sirita.rps.cpl'
    _description = 'Capaian Pembelajaran Lulusan (CPL)'
    _order = 'kode asc'

    kode = fields.Char(string='Kode CPL', required=True)
    name = fields.Text(string='Deskripsi CPL', required=True)
    prodi_id = fields.Many2one('hr.department', string='Program Studi', domain="[('department_type', '=', 'prodi')]", required=True)
