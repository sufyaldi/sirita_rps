# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SiritaRps(models.Model):
    _name = 'sirita.rps'
    _description = 'Rencana Pembelajaran Semester (RPS)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nomor Dokumen', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    prodi_id = fields.Many2one('hr.department', string='Program Studi', domain="[('department_type', '=', 'prodi')]", required=True, tracking=True)
    kurikulum_id = fields.Many2one('sirita.rps.kurikulum', string='Tahun Kurikulum', required=True, tracking=True)
    matkul_id = fields.Many2one('sirita.rps.course', string='Mata Kuliah', required=True, tracking=True)
    kode_mk = fields.Char(related='matkul_id.kode', string='Kode Mata Kuliah', readonly=True)
    sks = fields.Integer(related='matkul_id.sks', string='SKS', readonly=True)
    
    dosen_ids = fields.Many2many('hr.employee', 'sirita_rps_employee_rel', 'rps_id', 'employee_id', string='Dosen Tim Pengembang', tracking=True)
    koordinator_id = fields.Many2one('hr.employee', string='Koordinator MK', tracking=True)
    metode_ids = fields.Many2many('sirita.rps.metode', 'sirita_rps_metode_rel', 'rps_id', 'metode_id', string='Metode Pembelajaran Utama')
    
    tanggal_penyusunan = fields.Date(string='Tanggal Penyusunan', default=fields.Date.context_today, required=True, tracking=True)
    deskripsi = fields.Text(string='Deskripsi Mata Kuliah')
    pustaka_utama = fields.Text(string='Pustaka Utama')
    pustaka_pendukung = fields.Text(string='Pustaka Pendukung')
    media_software = fields.Char(string='Media Perangkat Lunak')
    media_hardware = fields.Char(string='Media Perangkat Keras')
    
    cpmk_ids = fields.One2many('sirita.rps.cpmk', 'rps_id', string='CPMK')
    weekly_ids = fields.One2many('sirita.rps.weekly', 'rps_id', string='Materi Mingguan')
    
    state = fields.Selection([
        ('draft', 'Draf'),
        ('submitted', 'Menunggu Validasi'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak')
    ], string='Status', default='draft', required=True, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sirita.rps') or _('New')
        return super(SiritaRps, self).create(vals_list)

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_draft(self):
        self.write({'state': 'draft'})
