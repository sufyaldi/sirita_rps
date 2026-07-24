# SIRITA RPS - Rencana Pembelajaran Semester 

[![Odoo Version](https://img.shields.io/badge/Odoo-19.0-875A7B.svg)](https://www.odoo.com/)


**SIRITA RPS** adalah modul Odoo 19 yang dirancang khusus untuk memfasilitasi pembuatan, pengelolaan, dan validasi dokumen **Rencana Pembelajaran Semester (RPS)** berbasis **Outcome-Based Education (OBE)** secara mandiri oleh dosen melalui portal frontend tanpa membutuhkan akses ke backend Odoo.

---

## 🚀 Fitur Utama

- **Portal Pembuatan RPS Mandiri**: Dosen dapat masuk ke portal Odoo dan membuat draf RPS baru secara instan dengan memilih mata kuliah yang terintegrasi dari database akademik.
- **Standarisasi Metode Pembelajaran OBE**: Menyediakan 14 pilihan metode pembelajaran prioritas sesuai standar SN-Dikti (seperti *Problem-Based Learning*, *Project-Based Learning*, *Case-Based Learning*, *Small Group Discussion*, dll.) yang terhubung ke header RPS.
- **Manajemen CPMK (Capaian Pembelajaran Mata Kuliah)**: Pendefinisian CPMK yang terintegrasi dengan CPL (Capaian Pembelajaran Lulusan) Program Studi beserta bobot penilaian.
- **Rencana Pertemuan 16 Minggu**: Penyusunan aktivitas mingguan terperinci yang mencakup Sub-CPMK, Bahan Kajian, Metode Pembelajaran spesifik, Indikator, Kriteria Penilaian, dan Bobot Nilai.
- **Workflow Validasi**: Alur penyerahan draf RPS oleh dosen pengampu dan validasi dokumen oleh Koordinator Program Studi/Mata Kuliah.
- **Antarmuka Premium**: Menggunakan penataan CSS/SCSS kustom dengan estetika modern, responsif, dan ramah pengguna di portal Odoo.

---

## 📁 Struktur Folder Modul

```text
sirita_rps/
├── controllers/
│   ├── __init__.py
│   └── portal.py              # Routing portal frontend untuk manajemen & pembuatan RPS
├── data/
│   ├── sirita_rps_data.xml    # Sequence nomor dokumen RPS
│   └── sirita_rps_metode_data.xml # Seed data 14 metode pembelajaran SN-Dikti
├── models/
│   ├── __init__.py
│   ├── rps.py                 # Model utama dokumen RPS
│   ├── rps_cpmk.py            # Model Capaian Pembelajaran Mata Kuliah (CPMK)
│   ├── rps_metode.py          # Model pustaka Metode Pembelajaran OBE
│   └── rps_weekly.py          # Model Rencana Pembelajaran Mingguan (16 minggu)
├── security/
│   ├── ir.model.access.csv    # Aturan hak akses model (ACL)
│   └── security.xml           # Aturan keamanan baris (Record Rules)
├── views/
│   ├── portal_templates.xml   # Template HTML/XML portal frontend kustom
│   └── rps_views.xml          # Form & Tree views backend Odoo 19
├── __init__.py
└── __manifest__.py            # Informasi manifest modul
```

---

## 🛠️ Instalasi

### Prasyarat
Modul ini bergantung pada modul master akademik:
- **`sirita_akademik`** (Menyediakan data mata kuliah, kurikulum, CPL, prodi, dan dosen)

### Langkah Pemasangan
1. Salin folder `sirita_rps` ke direktori *addons* Odoo Anda:
   ```bash
   cp -r sirita_rps /path/to/odoo/custom/addons/
   ```
2. Perbarui daftar modul di Odoo melalui menu pengembang (*Apps -> Update Apps List*).
3. Cari modul **SIRITA RPS** dan klik **Install**.
4. Modul secara otomatis akan mengisi data awal 14 metode pembelajaran standar SN-Dikti.

---

## 🧑‍💻 Penulis & Lisensi

- **Tim Pengembang**: Sufyaldy & UPT TIPD IAIN Parepare
- **Lisensi**: AGPL-3 
