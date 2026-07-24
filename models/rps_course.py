# -*- coding: utf-8 -*-

from odoo import models, fields

class SiritaRpsCourse(models.Model):
    _name = 'sirita.rps.course'
    _description = 'Mata Kuliah'
    _order = 'name asc'

    name = fields.Char(string='Nama Mata Kuliah', required=True)
    kode = fields.Char(string='Kode Mata Kuliah', required=True)
    sks = fields.Integer(string='SKS', default=2, required=True)
    prodi_id = fields.Many2one('hr.department', string='Program Studi', domain="[('department_type', '=', 'prodi')]", required=True)
    kurikulum_id = fields.Many2one('sirita.rps.kurikulum', string='Kurikulum', required=True)
