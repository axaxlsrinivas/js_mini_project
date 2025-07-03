import sqlite3
import datetime

DB_NAME = 'equipment.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Always create the table first if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            department TEXT,
            quantity INTEGER,
            details TEXT,
            condition_percent INTEGER,
            image_path TEXT
        )
    ''')
    # Now check for and add missing columns
    c.execute("PRAGMA table_info(equipment)")
    columns = [col[1] for col in c.fetchall()]
    if 'expiry_date' not in columns:
        c.execute('ALTER TABLE equipment ADD COLUMN expiry_date TEXT')
    if 'added_date' not in columns:
        c.execute('ALTER TABLE equipment ADD COLUMN added_date TEXT')
    # Sample data with expiry_date and added_date (YYYY-MM-DD)
    sample = [
        ('Syringe', '50 ml', 'General', 6327, 'Standard syringe', 90, '', '2026-01-01', '2024-01-01'),
        ('Surgical tweezers', 'General', 'Surgery', 2255, 'Precision tweezers', 80, '', '2025-08-01', '2023-08-01'),
        ('Scarifier', 'General', 'Laboratory', 7255, 'Blood sampling', 60, '', '2024-12-31', '2022-12-31'),
        ('Microscope', 'Electron', 'Laboratory', 1501, 'High-res microscope', 55, '', '2027-05-15', '2023-05-15'),
        ('Thermometer', 'Digital', 'General', 357, 'Digital thermometer', 95, '', '2025-07-01', '2024-07-01'),
        ('Stethophonendoscope', 'General', 'General', 500, 'Classic stethoscope', 85, '', '2026-11-11', '2023-11-11'),
        ('Disposable gloves', 'General', 'General', 10000, 'Latex gloves', 99, '', '2025-07-02', '2024-07-02'),
        ('Shoe covers', 'General', 'General', 30000, 'Disposable covers', 98, '', '2025-12-31', '2024-01-15')
    ]
    c.executemany('''
        INSERT INTO equipment (name, type, department, quantity, details, condition_percent, image_path, expiry_date, added_date)
        SELECT ?,?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM equipment WHERE name=?)
    ''', [(n, t, d, q, de, cp, ip, ed, ad, n) for n, t, d, q, de, cp, ip, ed, ad in sample])
    conn.commit()
    conn.close()

def get_all_equipment():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM equipment')
    rows = c.fetchall()
    conn.close()
    return rows

def get_nonexpired_equipment():
    today = datetime.date.today().isoformat()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM equipment WHERE expiry_date IS NULL OR expiry_date > ?', (today,))
    rows = c.fetchall()
    conn.close()
    return rows

def search_equipment(keyword):
    import datetime
    today = datetime.date.today().isoformat()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM equipment WHERE name LIKE ? AND (expiry_date IS NULL OR expiry_date > ?)', (f'%{keyword}%', today))
    rows = c.fetchall()
    conn.close()
    return rows

def get_equipment_by_id(equip_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM equipment WHERE id=?', (equip_id,))
    row = c.fetchone()
    conn.close()
    return row
