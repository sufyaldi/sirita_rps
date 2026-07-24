import psycopg2
import logging

_logger = logging.getLogger('fix_fkeys')

dbs = ['websiteiainpare_temp', 'tipd19.3', 'tipd19']

queries = [
    # Fix matkul_id
    'ALTER TABLE sirita_rps DROP CONSTRAINT IF EXISTS sirita_rps_matkul_id_fkey',
    'ALTER TABLE sirita_rps ADD CONSTRAINT sirita_rps_matkul_id_fkey FOREIGN KEY (matkul_id) REFERENCES sim_akademik_mata_kuliah(id) ON DELETE RESTRICT',
    # Fix kurikulum_id
    'ALTER TABLE sirita_rps DROP CONSTRAINT IF EXISTS sirita_rps_kurikulum_id_fkey',
    'ALTER TABLE sirita_rps ADD CONSTRAINT sirita_rps_kurikulum_id_fkey FOREIGN KEY (kurikulum_id) REFERENCES sim_akademik_kurikulum(id) ON DELETE RESTRICT',
    # Fix cpl_id in cpmk rel
    'ALTER TABLE sirita_rps_cpmk_cpl_rel DROP CONSTRAINT IF EXISTS sirita_rps_cpmk_cpl_rel_cpl_id_fkey',
    'ALTER TABLE sirita_rps_cpmk_cpl_rel ADD CONSTRAINT sirita_rps_cpmk_cpl_rel_cpl_id_fkey FOREIGN KEY (cpl_id) REFERENCES sim_akademik_cpl(id) ON DELETE CASCADE'
]

for db in dbs:
    try:
        conn = psycopg2.connect(f"dbname={db} user=odoo password=odoo host=db")
        cur = conn.cursor()
        for q in queries:
            cur.execute(q)
        conn.commit()
        cur.close()
        conn.close()
        print(f"FIXED FOREIGN KEYS SUCCESS ON: {db}")
    except Exception as e:
        print(f"ERROR ON {db}: {e}")
