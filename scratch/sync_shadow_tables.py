import psycopg2

dbs = ['websiteiainpare_temp', 'tipd19.3', 'tipd19']

for db in dbs:
    try:
        conn = psycopg2.connect(f"dbname={db} user=odoo password=odoo host=db")
        cur = conn.cursor()
        
        # Ensure shadow tables exist
        cur.execute("CREATE TABLE IF NOT EXISTS sirita_rps_kurikulum (id integer PRIMARY KEY, name varchar)")
        cur.execute("CREATE TABLE IF NOT EXISTS sirita_rps_course (id integer PRIMARY KEY, name varchar, kode varchar, sks integer, prodi_id integer, kurikulum_id integer)")
        
        # Copy from academic to shadow tables to satisfy base module foreign keys
        cur.execute("""
            INSERT INTO sirita_rps_kurikulum (id, name)
            SELECT id, name FROM sim_akademik_kurikulum
            ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name
        """)
        
        cur.execute("""
            INSERT INTO sirita_rps_course (id, name, kode, sks, prodi_id, kurikulum_id)
            SELECT id, name, kode, sks, prodi_id, kurikulum_id FROM sim_akademik_mata_kuliah
            ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name, kode=EXCLUDED.kode, sks=EXCLUDED.sks, prodi_id=EXCLUDED.prodi_id, kurikulum_id=EXCLUDED.kurikulum_id
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"SHADOW TABLES SYNCED SUCCESS ON: {db}")
    except Exception as e:
        print(f"ERROR ON {db}: {e}")
