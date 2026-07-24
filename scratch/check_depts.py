import os
import psycopg2

def check():
    conn = psycopg2.connect("dbname=tipd19 user=odoo password=odoo host=db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, kode, kurikulum_id FROM sim_akademik_mata_kuliah LIMIT 10")
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Kode: {row[2]}, Kurikulum ID: {row[3]}")
    cur.close()
    conn.close()

if __name__ == "__main__":
    check()
