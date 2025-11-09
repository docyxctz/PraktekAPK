import customtkinter as ctk
from tkinter import messagebox
from manajer_basis_data import ManajerBasisData
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Warna tema
THEME_GREEN = "#4CAF50"
THEME_BLUE = "#1E88E5"

# --- DASHBOARD FRAME (Grafik, Input, Pengingat) ---
class FrameDasbor(ctk.CTkFrame):
    def __init__(self, master, manajer_db: ManajerBasisData, id_pengguna):
        super().__init__(master, fg_color="transparent")
        self.manajer_db = manajer_db
        self.id_pengguna = id_pengguna
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Frame Kiri: Grafik Histori
        self.frame_grafik = ctk.CTkFrame(self, corner_radius=10)
        self.frame_grafik.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_grafik.grid_columnconfigure(0, weight=1)
        self.frame_grafik.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(self.frame_grafik, text="Riwayat Berat Badan & Kalori", font=ctk.CTkFont(size=18, weight="bold"), text_color=THEME_BLUE).grid(row=0, column=0, pady=(15, 5))
        self.gambar_grafik(self.frame_grafik)

        # Frame Kanan: Input Data & Pengingat
        self.frame_input_pengingat = ctk.CTkFrame(self, corner_radius=10)
        self.frame_input_pengingat.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_input_pengingat.grid_columnconfigure(0, weight=1)

        self.buat_bagian_input(self.frame_input_pengingat)
        self.buat_bagian_pengingat(self.frame_input_pengingat)

    def gambar_grafik(self, master_frame):
        """Membuat dan menampilkan grafik menggunakan Matplotlib."""
        riwayat_data = self.manajer_db.dapatkan_riwayat_kesehatan(self.id_pengguna)
        
        tanggal = [item[0] for item in riwayat_data]
        berat = [item[1] for item in riwayat_data]
        kalori = [item[2] for item in riwayat_data]
        
        # Jika tidak ada data, tampilkan pesan
        if not tanggal:
            ctk.CTkLabel(master_frame, text="Tidak ada data kesehatan yang tersedia.", text_color="gray").grid(row=1, column=0, padx=20, pady=20)
            return

        fig, ax1 = plt.subplots(figsize=(6, 4), dpi=100)
        
        # Pengaturan Tema Matplotlib agar sesuai CustomTkinter (Dark)
        fig.patch.set_facecolor('#242424')
        ax1.set_facecolor('#242424')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax1.spines['left'].set_color('white')
        ax1.spines['bottom'].set_color('white')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # Plot Berat Badan (Biru)
        ax1.plot(tanggal, berat, color=THEME_BLUE, marker='o', label='Berat (kg)')
        ax1.set_ylabel('Berat Badan (kg)', color=THEME_BLUE)
        ax1.tick_params(axis='y', labelcolor=THEME_BLUE)
        
        # Plot Kalori (Hijau) - Sumbu Y kedua
        ax2 = ax1.twinx()
        ax2.plot(tanggal, kalori, color=THEME_GREEN, marker='x', linestyle='--', label='Kalori (kcal)')
        ax2.set_ylabel('Kalori (kcal)', color=THEME_GREEN)
        ax2.tick_params(axis='y', labelcolor=THEME_GREEN)
        
        ax1.set_xlabel('Tanggal', color='white')
        ax1.set_title('Progres Kesehatan', color='white')
        
        # Penyesuaian sumbu X (hanya tampilkan beberapa label)
        step = max(1, len(tanggal) // 7)
        ax1.set_xticks(tanggal[::step])
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Integrasi ke CustomTkinter
        kanvas = FigureCanvasTkAgg(fig, master=master_frame)
        widget_kanvas = kanvas.get_tk_widget()
        widget_kanvas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def buat_bagian_input(self, master_frame):
        """Bagian untuk input data harian."""
        frame_input = ctk.CTkFrame(master_frame, corner_radius=10, fg_color="#2e2e2e")
        frame_input.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(frame_input, text="Input Data Harian", font=ctk.CTkFont(size=16, weight="bold"), text_color="white").grid(row=0, column=0, columnspan=2, pady=(10, 5))

        ctk.CTkLabel(frame_input, text="Berat (kg):", text_color="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entri_berat = ctk.CTkEntry(frame_input, width=100)
        self.entri_berat.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        ctk.CTkLabel(frame_input, text="Kalori Masuk (kcal):", text_color="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entri_kalori = ctk.CTkEntry(frame_input, width=100)
        self.entri_kalori.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        
        tombol_simpan = ctk.CTkButton(frame_input, text="Simpan Data", command=self.simpan_data, fg_color=THEME_GREEN, hover_color="#388E3C")
        tombol_simpan.grid(row=3, column=0, columnspan=2, pady=(10, 15))

    def simpan_data(self):
        try:
            berat = float(self.entri_berat.get())
            kalori = float(self.entri_kalori.get())
            
            if berat <= 0 or kalori < 0:
                raise ValueError
                
            self.manajer_db.simpan_data_kesehatan(self.id_pengguna, berat, kalori)
            # Karena grafik tidak diperbarui secara otomatis, pesan ini mengarahkan pengguna
            messagebox.showinfo("Sukses", "Data harian berhasil disimpan! Mohon navigasi ulang untuk memuat ulang grafik.")
            
        except ValueError:
            messagebox.showerror("Error", "Input Berat dan Kalori harus angka positif.")

    def buat_bagian_pengingat(self, master_frame):
        """Bagian Pengingat Minum."""
        frame_pengingat = ctk.CTkFrame(master_frame, corner_radius=10, fg_color="#2e2e2e")
        frame_pengingat.pack(fill="x", padx=10, pady=(5, 10))
        
        ctk.CTkLabel(frame_pengingat, text="💧 Pengingat Minum 💧", font=ctk.CTkFont(size=16, weight="bold"), text_color=THEME_BLUE).pack(pady=(10, 5))
        ctk.CTkLabel(frame_pengingat, text="Anda perlu minum ~8 gelas air hari ini.", text_color="white").pack(pady=5)
        
        # Simulasikan progres minum
        self.progres_air = ctk.CTkProgressBar(frame_pengingat, orientation="horizontal", progress_color=THEME_BLUE)
        self.progres_air.set(0.3)
        self.progres_air.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame_pengingat, text="Progres: 3 dari 8 Gelas", text_color="white").pack(pady=(0, 10))


# --- TARGET FRAME (Kalender, Saran) ---
class FrameTarget(ctk.CTkFrame):
    def __init__(self, master, manajer_db: ManajerBasisData, id_pengguna):
        super().__init__(master, fg_color="transparent")
        self.manajer_db = manajer_db
        self.id_pengguna = id_pengguna
        
        ctk.CTkLabel(self, text="MENU TARGET KESEHATAN", font=ctk.CTkFont(size=20, weight="bold"), text_color=THEME_GREEN).pack(pady=20)
        
        # Wadah untuk input target
        frame_input_target = ctk.CTkFrame(self)
        frame_input_target.pack(pady=10, padx=20)
        
        ctk.CTkLabel(frame_input_target, text="Tujuan Anda:", text_color="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.variabel_target = ctk.StringVar(value="Menjaga Berat Badan")
        pilihan_target = ctk.CTkOptionMenu(frame_input_target, values=["Menurunkan Berat Badan", "Menjaga Berat Badan", "Menambah Berat Badan"], 
                                          variable=self.variabel_target)
        pilihan_target.grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(frame_input_target, text="Lama Waktu (hari, min 7):", text_color="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entri_durasi = ctk.CTkEntry(frame_input_target, width=100)
        self.entri_durasi.grid(row=1, column=1, padx=10, pady=5)
        self.entri_durasi.insert(0, "7")
        
        ctk.CTkButton(frame_input_target, text="Buat Target & Saran", command=self.buat_target_dan_saran, fg_color=THEME_BLUE, hover_color="#1565C0").grid(row=2, column=0, columnspan=2, pady=10)

        # Wadah untuk hasil/saran
        self.frame_saran = ctk.CTkScrollableFrame(self, label_text="Saran Harian (Contoh)", height=300)
        self.frame_saran.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkLabel(self.frame_saran, text="Masukkan tujuan dan durasi untuk melihat saran harian.", text_color="gray").pack(pady=20)

    def buat_target_dan_saran(self):
        """Membuat target dan memberikan saran olahraga/makanan."""
        try:
            durasi = int(self.entri_durasi.get())
            if durasi < 7:
                messagebox.showerror("Error", "Lama waktu minimal harus 7 hari.")
                return
        except ValueError:
            messagebox.showerror("Error", "Lama waktu harus berupa angka.")
            return

        target = self.variabel_target.get()
        
        # Bersihkan frame saran
        for widget in self.frame_saran.winfo_children():
            widget.destroy()

        # Logika Saran (Sederhana)
        if target == "Menurunkan Berat Badan":
            tugas_harian = "Defisit Kalori: Kurangi asupan kalori sebesar 500 kcal dari TDEE Anda (perlu dihitung)."
            saran_latihan_text = f"Tugas Latihan Harian: Lakukan Lari (Menengah) selama 30 menit."
            saran_makanan_text = f"Saran Makanan: Pilih Protein Tinggi (Ayam Dada) dan Sayuran Berserat (Brokoli)."
        elif target == "Menambah Berat Badan":
            tugas_harian = "Surplus Kalori: Tingkatkan asupan kalori sebesar 500 kcal dari TDEE Anda."
            saran_latihan_text = f"Tugas Latihan Harian: Fokus pada latihan kekuatan (angkat beban)."
            saran_makanan_text = f"Saran Makanan: Konsumsi Karbohidrat Padat (Nasi Putih) dan Protein Cukup."
        else: # Menjaga Berat Badan
            tugas_harian = "Keseimbangan Kalori: Pertahankan asupan kalori sama dengan TDEE Anda."
            saran_latihan_text = f"Tugas Latihan Harian: Gabungkan Bersepeda dan Yoga untuk keseimbangan."
            saran_makanan_text = f"Saran Makanan: Jaga porsi seimbang antara makronutrien."

        # Menampilkan hasil
        ctk.CTkLabel(self.frame_saran, text=f"Tujuan: {target}", font=ctk.CTkFont(size=16, weight="bold"), text_color=THEME_GREEN).pack(pady=(10, 5))
        ctk.CTkLabel(self.frame_saran, text=f"Durasi: {durasi} Hari", text_color="white").pack(pady=5)
        
        ctk.CTkLabel(self.frame_saran, text="--- Tugas Harian ---", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 0))
        ctk.CTkLabel(self.frame_saran, text=tugas_harian, wraplength=400, justify="left").pack(pady=5, padx=10)
        
        ctk.CTkLabel(self.frame_saran, text="--- Saran Latihan ---", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 0))
        ctk.CTkLabel(self.frame_saran, text=saran_latihan_text, wraplength=400, justify="left").pack(pady=5, padx=10)
        
        ctk.CTkLabel(self.frame_saran, text="--- Saran Makanan ---", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 0))
        ctk.CTkLabel(self.frame_saran, text=saran_makanan_text, wraplength=400, justify="left").pack(pady=5, padx=10)
        
        messagebox.showinfo("Target Sukses", f"Target untuk {durasi} hari telah dibuat!")


# --- INFO FRAME (Nilai Gizi & Olahraga) ---
class FrameInfo(ctk.CTkFrame):
    def __init__(self, master, manajer_db: ManajerBasisData, id_pengguna):
        super().__init__(master, fg_color="transparent")
        self.manajer_db = manajer_db
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        ctk.CTkLabel(self, text="MENU INFORMASI (NILAI GIZI & LATIHAN)", font=ctk.CTkFont(size=20, weight="bold"), text_color=THEME_GREEN).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="n")

        self.tampilkan_daftar_gizi()
        self.tampilkan_daftar_latihan()

    def tampilkan_daftar_gizi(self):
        """Menampilkan daftar Nilai Gizi Makanan."""
        frame_gizi = ctk.CTkFrame(self, corner_radius=10)
        frame_gizi.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        frame_gizi.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame_gizi, text="Daftar Nilai Gizi Makanan", font=ctk.CTkFont(size=16, weight="bold"), text_color=THEME_BLUE).pack(pady=10)
        
        frame_gulir = ctk.CTkScrollableFrame(frame_gizi, width=350, height=300)
        frame_gulir.pack(padx=10, pady=5, fill="both", expand=True)

        data = self.manajer_db.dapatkan_daftar_gizi()
        
        # Header Tabel
        header = ["Nama", "Kalori", "Protein", "Lemak", "Karbo"]
        for i, h in enumerate(header):
            ctk.CTkLabel(frame_gulir, text=h, font=ctk.CTkFont(weight="bold"), text_color=THEME_GREEN).grid(row=0, column=i, padx=5, pady=5)
            
        # Isi Tabel
        for indeks_baris, item in enumerate(data):
            ctk.CTkLabel(frame_gulir, text=item['name'], justify="left").grid(row=indeks_baris+1, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(frame_gulir, text=f"{item['calories']:.0f}").grid(row=indeks_baris+1, column=1, padx=5, pady=2)
            ctk.CTkLabel(frame_gulir, text=f"{item['protein']:.1f}g").grid(row=indeks_baris+1, column=2, padx=5, pady=2)
            ctk.CTkLabel(frame_gulir, text=f"{item['fat']:.1f}g").grid(row=indeks_baris+1, column=3, padx=5, pady=2)
            ctk.CTkLabel(frame_gulir, text=f"{item['carbs']:.1f}g").grid(row=indeks_baris+1, column=4, padx=5, pady=2)
            

    def tampilkan_daftar_latihan(self):
        """Menampilkan daftar Olahraga."""
        frame_latihan = ctk.CTkFrame(self, corner_radius=10)
        frame_latihan.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        frame_latihan.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame_latihan, text="Daftar Latihan", font=ctk.CTkFont(size=16, weight="bold"), text_color=THEME_BLUE).pack(pady=10)
        
        frame_gulir = ctk.CTkScrollableFrame(frame_latihan, width=350, height=300)
        frame_gulir.pack(padx=10, pady=5, fill="both", expand=True)

        data = self.manajer_db.dapatkan_daftar_latihan()
        
        # Header Tabel
        ctk.CTkLabel(frame_gulir, text="Nama Latihan", font=ctk.CTkFont(weight="bold"), text_color=THEME_GREEN).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(frame_gulir, text="Kalori/Jam", font=ctk.CTkFont(weight="bold"), text_color=THEME_GREEN).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame_gulir, text="Deskripsi", font=ctk.CTkFont(weight="bold"), text_color=THEME_GREEN).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Isi Tabel
        for indeks_baris, item in enumerate(data):
            ctk.CTkLabel(frame_gulir, text=item['name'], justify="left").grid(row=indeks_baris+1, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(frame_gulir, text=f"{item['calories_burned_per_hour']:.0f}").grid(row=indeks_baris+1, column=1, padx=5, pady=2)
            ctk.CTkLabel(frame_gulir, text=item['description'], wraplength=200, justify="left").grid(row=indeks_baris+1, column=2, padx=5, pady=2, sticky="w")


# --- PROFILE FRAME (Update Profil) ---
class FrameProfil(ctk.CTkFrame):
    def __init__(self, master, manajer_db: ManajerBasisData, id_pengguna):
        super().__init__(master, fg_color="transparent")
        self.manajer_db = manajer_db
        self.id_pengguna = id_pengguna
        
        self.data_pengguna = self.manajer_db.dapatkan_data_pengguna(self.id_pengguna)
        
        ctk.CTkLabel(self, text="MENU PROFIL PENGGUNA", font=ctk.CTkFont(size=20, weight="bold"), text_color=THEME_GREEN).pack(pady=20)
        
        # Wadah input
        frame_input = ctk.CTkFrame(self, corner_radius=10)
        frame_input.pack(pady=10, padx=20)
        
        def safe_get(key):
            """Mengambil nilai dari data pengguna, mengembalikan '' jika None atau tidak ada."""
            val = self.data_pengguna.get(key)
            # Pastikan nilai numerik yang None tidak diubah menjadi string 'None'
            return str(val) if val is not None and val != '' else ''

        # Nama Pengguna (Hanya baca)
        ctk.CTkLabel(frame_input, text="Nama Pengguna (ID):", text_color="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(frame_input, text=f"ID: {self.data_pengguna.get('id', 'N/A')} - {self.data_pengguna.get('username', 'N/A')}", text_color=THEME_BLUE).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Nama Lengkap
        ctk.CTkLabel(frame_input, text="Nama Lengkap:", text_color="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entri_nama_lengkap = ctk.CTkEntry(frame_input, width=200)
        self.entri_nama_lengkap.grid(row=1, column=1, padx=10, pady=5)
        self.entri_nama_lengkap.insert(0, safe_get('full_name'))

        # Berat Awal
        ctk.CTkLabel(frame_input, text="Berat Awal (kg):", text_color="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entri_berat_awal = ctk.CTkEntry(frame_input, width=200)
        self.entri_berat_awal.grid(row=2, column=1, padx=10, pady=5)
        self.entri_berat_awal.insert(0, safe_get('initial_weight'))

        # Tinggi Badan
        ctk.CTkLabel(frame_input, text="Tinggi (cm):", text_color="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entri_tinggi = ctk.CTkEntry(frame_input, width=200)
        self.entri_tinggi.grid(row=3, column=1, padx=10, pady=5)
        self.entri_tinggi.insert(0, safe_get('height'))

        # Target Berat
        ctk.CTkLabel(frame_input, text="Target Berat (kg):", text_color="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entri_berat_target = ctk.CTkEntry(frame_input, width=200)
        self.entri_berat_target.grid(row=4, column=1, padx=10, pady=5)
        self.entri_berat_target.insert(0, safe_get('target_weight'))

        tombol_perbarui = ctk.CTkButton(frame_input, text="Perbarui Profil", command=self.perbarui_profil, fg_color=THEME_GREEN, hover_color="#388E3C")
        tombol_perbarui.grid(row=5, column=0, columnspan=2, pady=15)

    def perbarui_profil(self):
        nama = self.entri_nama_lengkap.get()
        berat_awal = self.entri_berat_awal.get()
        tinggi = self.entri_tinggi.get()
        berat_target = self.entri_berat_target.get()
        
        try:
            # Mengonversi string ke float; jika string kosong, set menjadi None
            berat_awal_val = float(berat_awal) if berat_awal.strip() else None
            tinggi_val = float(tinggi) if tinggi.strip() else None
            berat_target_val = float(berat_target) if berat_target.strip() else None
            
            self.manajer_db.kursor.execute("""
                UPDATE users SET 
                full_name = ?, 
                initial_weight = ?, 
                height = ?, 
                target_weight = ?
                WHERE id = ?
            """, (nama, berat_awal_val, tinggi_val, berat_target_val, self.id_pengguna))
            self.manajer_db.koneksi.commit()
            messagebox.showinfo("Sukses", "Profil berhasil diperbarui!")
            
        except ValueError:
            messagebox.showerror("Error", "Berat dan Tinggi harus berupa angka yang valid.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")