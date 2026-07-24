# Seeding script for sim.akademik.kurikulum
import logging

_logger = logging.getLogger('odoo.shell')

# Create Kurikulum 2025 and 2026
k2025 = env['sim.akademik.kurikulum'].search([('name', '=', 'Kurikulum 2025')], limit=1)
if not k2025:
    k2025 = env['sim.akademik.kurikulum'].create({
        'name': 'Kurikulum 2025',
        'kode': 'K2025',
        'aktif': True
    })
    _logger.info("Created Kurikulum 2025")

k2026 = env['sim.akademik.kurikulum'].search([('name', '=', 'Kurikulum 2026')], limit=1)
if not k2026:
    k2026 = env['sim.akademik.kurikulum'].create({
        'name': 'Kurikulum 2026',
        'kode': 'K2026',
        'aktif': True
    })
    _logger.info("Created Kurikulum 2026")

# Now link mata kuliah to kurikulum
courses_2026 = env['sim.akademik.mata.kuliah'].search([('kode', 'like', 'PPSSI26%')])
courses_2026.write({'kurikulum_id': k2026.id})
_logger.info(f"Linked {len(courses_2026)} courses to Kurikulum 2026")

courses_2025 = env['sim.akademik.mata.kuliah'].search([('kode', 'not like', 'PPSSI26%')])
courses_2025.write({'kurikulum_id': k2025.id})
_logger.info(f"Linked {len(courses_2025)} courses to Kurikulum 2025")

env.cr.commit()
print("KURIKULUM SEEDED AND LINKED SUCCESSFULLY")
