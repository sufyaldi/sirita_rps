# -*- coding: utf-8 -*-

from odoo import models, fields

class SiritaRpsCpmk(models.Model):
    _name = 'sirita.rps.cpmk'
    _description = 'Capaian Pembelajaran Mata Kuliah (CPMK) RPS'
    _order = 'kode'

    rps_id = fields.Many2one('sirita.rps', string='RPS', ondelete='cascade', required=True)
    kode = fields.Char(string='Kode CPMK', required=True, placeholder="Contoh: CPMK-01")
    name = fields.Text(string='Deskripsi/Kemampuan Akhir', required=True)
    bobot = fields.Float(string='Bobot (%)', default=0.0)
    cpl_ids = fields.Many2many('sirita.rps.cpl', 'sirita_rps_cpmk_cpl_rel', 'cpmk_id', 'cpl_id', string='CPL yang Dipenuhi')
