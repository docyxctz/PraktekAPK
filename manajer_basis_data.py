import sqlite3
from datetime import datetime

class ManajerBasisData:
    """Mengelola koneksi dan interaksi dengan basis data SQLite."""
    
    def __init__(self, nama_db='aplikasi_kesehatan.db'):
        self.koneksi = sqlite3.connect(nama_db)
        self.koneksi.row_factory = sqlite3.Row # Mengizinkan akses kolom berdasarkan nama
        self.kursor = self.koneksi.cursor()
        self.buat_tabel()

    def buat_tabel(self):
        """Membuat tabel pengguna, riwayat kesehatan, nutrisi, dan latihan jika belum ada."""
        
        # Tabel Pengguna
        self.kursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL, -- 'user' atau 'admin'
                full_name TEXT,
                initial_weight REAL,
                height REAL,
                target_weight REAL
            )
        """)

        # Tabel Riwayat Kesehatan (Pencatatan harian)
        self.kursor.execute("""
            CREATE TABLE IF NOT EXISTS health_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                weight REAL,
                calories_intake REAL,
                UNIQUE(user_id, date),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Tabel Nilai Gizi Makanan (untuk Admin)
        self.kursor.execute("""
            CREATE TABLE IF NOT EXISTS nutrition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                calories REAL,
                protein REAL,
                fat REAL,
                carbs REAL
            )
        """)
        
        # Tabel Olahraga (untuk Admin)
        self.kursor.execute("""
            CREATE TABLE IF NOT EXISTS exercise (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                calories_burned_per_hour REAL,
                description TEXT
            )
        """)

        self.koneksi.commit()

        # Tambahkan Admin default jika belum ada
        if not self.kursor.execute("SELECT id FROM users WHERE role = 'admin'").fetchone():
            self.tambah_pengguna("admin", "admin123", "admin")

        # Tambahkan data nutrisi default jika kosong
        if not self.kursor.execute("SELECT id FROM nutrition").fetchone():
            self.update_gizi("Nasi Putih", 130, 2.7, 0.3, 28)
            self.update_gizi("Ayam Panggang", 165, 31, 3.6, 0)
            self.update_gizi("Brokoli Kukus", 34, 2.8, 0.4, 6.6)
            
        # Tambahkan data latihan default jika kosong
        if not self.kursor.execute("SELECT id FROM exercise").fetchone():
            self.update_latihan("Lari (Menengah)", 590, "Lari dengan kecepatan stabil selama 1 jam.")
            self.update_latihan("Bersepeda", 500, "Bersepeda santai hingga sedang.")
            self.update_latihan("Yoga", 250, "Sesi yoga ringan/meditasi.")

    def tambah_pengguna(self, nama_pengguna, kata_sandi, peran='user'):
        """Menambahkan pengguna baru."""
        try:
            self.kursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                                (nama_pengguna, kata_sandi, peran))
            self.koneksi.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Nama pengguna sudah ada

    def autentikasi_pengguna(self, nama_pengguna, kata_sandi):
        """Memeriksa kredensial pengguna dan mengembalikan ID dan peran."""
        self.kursor.execute("SELECT id, role FROM users WHERE username = ? AND password = ?", 
                            (nama_pengguna, kata_sandi))
        hasil = self.kursor.fetchone()
        return dict(hasil) if hasil else None

    def dapatkan_data_pengguna(self, id_pengguna):
        """Mengambil data profil pengguna berdasarkan ID."""
        self.kursor.execute("SELECT * FROM users WHERE id = ?", (id_pengguna,))
        hasil = self.kursor.fetchone()
        return dict(hasil) if hasil else {}
        
    def dapatkan_semua_data_pengguna(self):
        """Mengambil data semua pengguna (untuk Admin)."""
        self.kursor.execute("SELECT * FROM users WHERE role = 'user'")
        return [dict(row) for row in self.kursor.fetchall()]

    def simpan_data_kesehatan(self, id_pengguna, berat, asupan_kalori):
        """Menyimpan atau memperbarui data kesehatan harian."""
        tanggal = datetime.now().strftime("%Y-%m-%d")
        
        # Cek apakah data untuk tanggal ini sudah ada
        self.kursor.execute("SELECT id FROM health_history WHERE user_id = ? AND date = ?", (id_pengguna, tanggal))
        data_lama = self.kursor.fetchone()
        
        if data_lama:
            # Perbarui data yang ada
            self.kursor.execute("""
                UPDATE health_history SET 
                weight = ?, 
                calories_intake = ?
                WHERE id = ?
            """, (berat, asupan_kalori, data_lama['id']))
        else:
            # Tambahkan data baru
            self.kursor.execute("""
                INSERT INTO health_history (user_id, date, weight, calories_intake) 
                VALUES (?, ?, ?, ?)
            """, (id_pengguna, tanggal, berat, asupan_kalori))
            
        self.koneksi.commit()

    def dapatkan_riwayat_kesehatan(self, id_pengguna, batas=30):
        """Mengambil riwayat berat dan kalori 30 hari terakhir."""
        self.kursor.execute("""
            SELECT date, weight, calories_intake 
            FROM health_history 
            WHERE user_id = ? 
            ORDER BY date DESC 
            LIMIT ?
        """, (id_pengguna, batas))
        
        # Kembalikan dalam urutan kronologis (terlama ke terbaru)
        riwayat = [dict(row) for row in self.kursor.fetchall()]
        # Format: [(tanggal, berat, kalori), ...]
        return [(item['date'], item['weight'], item['calories_intake']) for item in reversed(riwayat)]

    def update_gizi(self, nama, kalori, protein, lemak, karbo):
        """Menambahkan atau memperbarui data gizi (Admin)."""
        self.kursor.execute("""
            INSERT INTO nutrition (name, calories, protein, fat, carbs) 
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
            calories=excluded.calories, protein=excluded.protein, fat=excluded.fat, carbs=excluded.carbs
        """, (nama, kalori, protein, lemak, karbo))
        self.koneksi.commit()
        
    def dapatkan_daftar_gizi(self):
        """Mengambil semua daftar nutrisi."""
        self.kursor.execute("SELECT name, calories, protein, fat, carbs FROM nutrition ORDER BY name")
        return [dict(row) for row in self.kursor.fetchall()]

    def update_latihan(self, nama, kalori_terbakar_per_jam, deskripsi):
        """Menambahkan atau memperbarui data latihan (Admin)."""
        self.kursor.execute("""
            INSERT INTO exercise (name, calories_burned_per_hour, description) 
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
            calories_burned_per_hour=excluded.calories_burned_per_hour, description=excluded.description
        """, (nama, kalori_terbakar_per_jam, deskripsi))
        self.koneksi.commit()

    def dapatkan_daftar_latihan(self):
        """Mengambil semua daftar latihan."""
        self.kursor.execute("SELECT name, calories_burned_per_hour, description FROM exercise ORDER BY name")
        return [dict(row) for row in self.kursor.fetchall()]