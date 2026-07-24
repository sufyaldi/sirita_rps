# Script for Odoo Shell to insert courses
import logging

_logger = logging.getLogger('odoo.shell')

courses_data = [
    {"kode": "PPSSI263006", "name": "Filsafat Keilmuan Islam Lanjut", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Studi Islam"},
    {"kode": "PPSSI263007", "name": "Kajian Turats Islam Global dan Nusantara", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Studi Islam"},
    {"kode": "PPSSI263008", "name": "Rekonstruksi dan Pembaharuan Pemikiran Islam", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Studi Islam"},
    {"kode": "PPSSI263009", "name": "Metodologi Studi Islam Interdisipliner", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Studi Islam"},
    {"kode": "PPSSI263010", "name": "Seminar Peminatan Keahlian", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Studi Islam"},
    {"kode": "4003PAI", "name": "TESIS", "sks": 4, "jenis_mk": "Skripsi", "prodi_name": "Pendidikan Agama Islam"},
    {"kode": "EB25201", "name": "FILSAFAT EKONOMI ISLAM", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EB25202", "name": "STUDI AYAT EKONOMI", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EB25203", "name": "STUDI HADIS EKONOMI", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EB25204", "name": "FIQH MUAMALAH", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Ekonomi Syariah (Ekonomi Islam )"},
    {"kode": "EB25205", "name": "QAWAIDUL FIQHIYYAH FIL IQTISHAD", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EB25206", "name": "ETIKA BISNIS ISLAM", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Ekonomi Syariah (Ekonomi Islam )"},
    {"kode": "EB25307", "name": "BISNIS DAN MANAJEMEN", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EB25308", "name": "EKONOMI MIKRO ISLAM", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EB25309", "name": "EKONOMI MAKRO ISLAM", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EB25310", "name": "METODOLOGI PENELITIAN KUALITATIF", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EB25311", "name": "METODOLOGI PENELITIAN KUANTITATIF", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Ekonomi Syariah (Ekonomi Islam )"},
    {"kode": "EB25312", "name": "STATISTIKA", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Ekonomi Syariah (Ekonomi Islam )"},
    {"kode": "EB25313", "name": "ENTREPRENEURSHIP", "sks": 3, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EB25414", "name": "PPL", "sks": 4, "jenis_mk": "KKL", "prodi_name": "Perbankan Syariah"},
    {"kode": "EBA252001", "name": "PERPAJAKAN", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EBA252002", "name": "SISTEM MONETER ISLAM", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EBA252003", "name": "STUDI KELAYAKAN BISNIS", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EBA252004", "name": "AUDIT DAN PENGAWASAN BANK SYARIAH", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"},
    {"kode": "EBA252005", "name": "PASAR MODAL SYARIAH", "sks": 2, "jenis_mk": "Kuliah", "prodi_name": "Perbankan Syariah"}
]

for course in courses_data:
    # Find prodi
    prodi = env['hr.department'].search([('name', '=', course['prodi_name'])], limit=1)
    if not prodi:
        _logger.warning(f"Prodi not found: {course['prodi_name']}")
        continue
    
    # Check if course already exists
    existing = env['sim.akademik.mata.kuliah'].search([('kode', '=', course['kode'])], limit=1)
    
    vals = {
        'kode': course['kode'],
        'name': course['name'],
        'sks': course['sks'], # Set directly to satisfy database NotNull constraint
        'sks_tatap_muka': course['sks'],
        'jenis_mk': course['jenis_mk'],
        'prodi_id': prodi.id
    }
    
    if existing:
        existing.write(vals)
        _logger.info(f"Updated course: {course['kode']} - {course['name']}")
    else:
        env['sim.akademik.mata.kuliah'].create(vals)
        _logger.info(f"Created course: {course['kode']} - {course['name']}")

env.cr.commit()
print("SEEDED SUCCESSFULLY")
