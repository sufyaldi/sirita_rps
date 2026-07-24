# -*- coding: utf-8 -*-

from odoo import models, fields

class SiritaRpsWeekly(models.Model):
    _name = 'sirita.rps.weekly'
    _description = 'Materi Mingguan RPS'
    _order = 'week'

    rps_id = fields.Many2one('sirita.rps', string='RPS', ondelete='cascade', required=True)
    week = fields.Integer(string='Pertemuan Ke-', required=True, default=1)
    
    sub_cpmk = fields.Text(string='Kemampuan Akhir (Sub-CPMK)', required=True)
    bahan_kajian = fields.Text(string='Bahan Kajian / Materi Pembelajaran')
    metode_pembelajaran = fields.Text(string='Metode Pembelajaran')
    indikator = fields.Text(string='Indikator Penilaian')
    kriteria = fields.Text(string='Kriteria & Bentuk Penilaian')
    bobot = fields.Float(string='Bobot Penilaian (%)', default=0.0)
    
    cpmk_ids = fields.Many2many('sirita.rps.cpmk', 'sirita_rps_weekly_cpmk_rel', 'weekly_id', 'cpmk_id', string='Referensi CPMK')
