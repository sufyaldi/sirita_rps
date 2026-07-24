# -*- coding: utf-8 -*-
{
    'name': 'SIRITA RPS & OBE Portal',
    'version': '1.0',
    'category': 'Academic',
    'summary': 'Portal Penyusunan RPS Berbasis OBE - IAIN Parepare',
    'description': """
        Modul Odoo 19 untuk mengelola Rencana Pembelajaran Semester (RPS) 
        berbasis Outcome-Based Education (OBE) secara interaktif di portal frontend.
    """,
    'author': 'Sufyaldy | TIPD IAIN Parepare',
    'depends': ['base', 'website', 'portal', 'hr'],
    'data': [
        'data/sirita_rps_data.xml',
        'data/sirita_rps_metode_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/rps_views.xml',
        'views/portal_templates.xml',
        'views/sirita_rps_menu_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sirita_rps/static/src/scss/portal_rps.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
