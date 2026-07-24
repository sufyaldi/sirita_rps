# -*- coding: utf-8 -*-

prodi_data = [
    ("62201", "Akuntansi Lembaga Keuangan Syariah", True, "S1", "Unggul"),
    ("62202", "Akuntansi Syari`ah", True, "S1", "Unggul"),
    ("79203", "Bahasa dan Sastra Arab", True, "S1", "Baik Sekali"),
    ("70232", "Bimbingan Konseling Islam", True, "S1", "Baik Sekali"),
    ("60102", "Ekonomi Syari'ah", True, "S2", "Baik Sekali"),
    ("60202", "Ekonomi Syariah (Ekonomi Islam )", True, "S1", "Baik Sekali"),
    ("74234", "Hukum Ekonomi Syariah (Muamalah)", True, "S1", "Unggul"),
    ("74130", "Hukum Keluarga Islam (Ahwal Asy-Syakhshiyah)", True, "S2", "Unggul"),
    ("74230", "Hukum Keluarga Islam (Ahwal Syakhshiyyah)", True, "S1", "Unggul"),
    ("74231", "Hukum Pidana Islam (JInayah)", True, "S1", "Unggul"),
    ("74235", "Hukum Tatanegara (Siyasah)", True, "S1", "Baik"),
    ("74101", "Ilmu Syariah", False, "S2", "-"),
    ("70202", "Jurnalistik Islam", True, "S1", "Unggul"),
    ("70133", "Komunikasi dan Penyiaran Islam", True, "S2", "Baik Sekali"),
    ("70233", "Komunikasi Dan Penyiaran Islam", True, "S1", "Baik Sekali"),
    ("70230", "Manajemen Dakwah", True, "S1", "Baik Sekali"),
    ("61211", "Manajemen Keuangan Syariah", True, "S1", "Unggul"),
    ("86231", "Manajemen Pendidikan Islam", True, "S1", "Baik Sekali"),
    ("74236", "Manajemen Zakat dan Wakaf", True, "S1", "Unggul"),
    ("93202", "Pariwisata Syariah", True, "S1", "Baik Sekali"),
    ("86207", "Pendidikan Islam Anak Usia Dini", True, "S1", "Unggul"),
    ("86208", "Pendidikan Agama Islam", True, "S1", "Unggul"),
    ("86108", "Pendidikan Agama Islam", True, "S2", "Unggul"),
    ("88204", "Pendidikan Bahasa Arab", True, "S1", "Baik Sekali"),
    ("88104", "Pendidikan Bahasa Arab", True, "S2", "Baik Sekali"),
    ("88203", "Pendidikan Bahasa Inggris", True, "S1", "Unggul"),
    ("86906", "Pendidikan Profesi Guru", True, "Profesi", "Terakreditasi Pertama"),
    ("70231", "Pengembangan Masyarakat Islam", True, "S1", "Baik Sekali"),
    ("61206", "Perbankan Syariah", True, "S1", "Baik Sekali"),
    ("80230", "Sejarah Peradaban Islam", True, "S1", "Unggul"),
    ("69201", "Sosiologi Agama", True, "S1", "Baik Sekali"),
    ("76007", "Studi Islam", True, "S3", "-"),
    ("79102", "Tadris Bahasa Inggris", True, "S2", "Baik Sekali"),
    ("84206", "Tadris IPA", True, "S1", "Unggul"),
    ("87220", "Tadris IPS", True, "S1", "Baik Sekali"),
    ("84202", "Tadris Matematika", True, "S1", "Unggul"),
]

for kode, name, active, jenjang, akreditasi in prodi_data:
    existing = env['hr.department'].search([('kode_prodi', '=', kode)], limit=1)
    vals = {
        'name': name,
        'kode_prodi': kode,
        'department_type': 'prodi',
        'active': active,
        'jenjang': jenjang,
        'akreditasi': akreditasi if akreditasi != '-' else False,
    }
    if existing:
        existing.write(vals)
        print(f"Updated: {name}")
    else:
        env['hr.department'].create(vals)
        print(f"Created: {name}")

env.cr.commit()
print("PRODI SEEDING COMPLETED SUCCESS!")
