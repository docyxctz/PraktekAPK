import customtkinter as ctk
from tkinter import messagebox
from manajer_basis_data import ManajerBasisData

# Warna tema
THEME_GREEN = "#4CAF50"
THEME_BLUE = "#1E88E5"

# --- USER VIEWER (Admin) ---
class PenampilPengguna(ctk.CTkFrame):
    def __init__(self, master, manajer_db: ManajerBasisData):
        super().__init__(master, corner_radius=10)
        self.manajer_db = manajer_db
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text="Data Seluruh Pengguna", font=ctk.CTkFont(size=18, weight="bold"), text_color=THEME_GREEN).pack(pady=10)
        
        self.daftar_tampilan = ctk.CTkScrollableFrame(self, label_text="Daftar Pengguna Aktif", width=700, height=400)
        self.daftar_tampilan.pack(padx=20, pady=10, fill="both", expand=True)
        self.muat_ulang_daftar()

    def muat_ulang_daftar(self):
        for widget in self.daftar_tampilan.winfo_children():
            widget.destroy()
            
        data = self.manajer_db.dapatkan_semua_data_pengguna()
        
        # Header Tabel
        header = ["ID", "Nama Pengguna", "Nama Lengkap", "B. Awal", "Tinggi", "B. Target"]
        for i, h in enumerate(header):
            ctk.CTkLabel(self.daftar_tampilan, text=h, font=ctk.CTkFont(weight="bold"), text_color=THEME_BLUE).grid(row=0, column=i, padx=8, pady=5)
            
        # Isi Tabel
        for indeks_baris, item in enumerate(data):
            # Pastikan None atau 0.0 ditampilkan sebagai '-'
            # Nilai-nilai numerik ini mungkin NULL di DB, jadi tangani dengan aman
            berat_awal = f"{item['initial_weight']:.1f}" if item['initial_weight'] else '-'
            tinggi = f"{item['height']:.0f}" if item['height'] else '-'
            berat_target = f"{item['target_weight']:.1f}" if item['target_weight'] else '-'
            
            ctk.CTkLabel(self.daftar_tampilan, text=item['id'], justify="left").grid(row=indeks_baris+1, column=0, padx=8, pady=2, sticky="w")
            ctk.CTkLabel(self.daftar_tampilan, text=item['username'], justify="left").grid(row=indeks_baris+1, column=1, padx=8, pady=2, sticky="w")
            ctk.CTkLabel(self.daftar_tampilan, text=item['full_name'] or '-', justify="left").grid(row=indeks_baris+1, column=2, padx=8, pady=2, sticky="w")
            ctk.CTkLabel(self.daftar_tampilan, text=f"{berat_awal} kg").grid(row=indeks_baris+1, column=3, padx=8, pady=2)
            ctk.CTkLabel(self.daftar_tampilan, text=f"{tinggi} cm").grid(row=indeks_baris+1, column=4, padx=8, pady=2)
            ctk.CTkLabel(self.daftar_tampilan, text=f"{berat_target} kg").grid(row=indeks_baris+1, column=5, padx=8, pady=2)


# --- ADMIN PROFILE FRAME (Dapat diubah) ---
class FrameProfilAdmin(ctk.CTkFrame):
    def __init__(self, master, manajer_db: ManajerBasisData, id_pengguna):
        super().__init__(master, fg_color="transparent")
        self.manajer_db = manajer_db
        self.id_pengguna = id_pengguna
        self.data_admin = self.manajer_db.dapatkan_data_pengguna(self.id_pengguna)
        
        ctk.CTkLabel(self, text="PROFIL ADMINISTRATOR", font=ctk.CTkFont(size=20, weight="bold"), text_color=THEME_GREEN).pack(pady=20)
        
        # Wadah input
        frame_input = ctk.CTkFrame(self, corner_radius=10)
        frame_input.pack(pady=10, padx=20)
        
        def safe_get(key):
            """Mengambil nilai, mengembalikan '' jika None."""
            val = self.data_admin.get(key)
            return str(val) if val is not None else ''

        # ID Pengguna (Hanya baca)
        ctk.CTkLabel(frame_input, text="ID Pengguna:", text_color="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(frame_input, text=safe_get('id'), text_color=THEME_BLUE).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Username
        ctk.CTkLabel(frame_input, text="Username:", text_color="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entri_username = ctk.CTkEntry(frame_input, width=200)
        self.entri_username.grid(row=1, column=1, padx=10, pady=5)
        self.entri_username.insert(0, safe_get('username'))

        # Nama Lengkap
        ctk.CTkLabel(frame_input, text="Nama Lengkap:", text_color="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entri_nama_lengkap = ctk.CTkEntry(frame_input, width=200)
        self.entri_nama_lengkap.grid(row=2, column=1, padx=10, pady=5)
        self.entri_nama_lengkap.insert(0, safe_get('full_name'))
        
        # Tombol Perbarui
        tombol_perbarui = ctk.CTkButton(frame_input, text="Perbarui Profil Admin", command=self.perbarui_profil, fg_color=THEME_GREEN, hover_color="#388E3C")
        tombol_perbarui.grid(row=3, column=0, columnspan=2, pady=15)

    def perbarui_profil(self):
        username = self.entri_username.get().strip()
        nama = self.entri_nama_lengkap.get().strip()
        
        if not username:
             messagebox.showerror("Error", "Username tidak boleh kosong.")
             return

        try:
            # Update hanya username dan full_name untuk admin
            self.manajer_db.kursor.execute("""
                UPDATE users SET 
                username = ?, 
                full_name = ?
                WHERE id = ?
            """, (username, nama, self.id_pengguna))
            self.manajer_db.koneksi.commit()
            messagebox.showinfo("Sukses", "Profil Administrator berhasil diperbarui!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat update: {e}")