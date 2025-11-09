import customtkinter as ctk
from tkinter import messagebox
from manajer_basis_data import ManajerBasisData

# Warna tema
THEME_GREEN = "#4CAF50"
THEME_BLUE = "#1E88E5"

class HalamanMasukDaftar(ctk.CTkFrame):
    """Frame untuk halaman Masuk dan Daftar Pengguna."""
    
    def __init__(self, master, manajer_db: ManajerBasisData, panggilan_balik_sukses):
        super().__init__(master)
        self.manajer_db = manajer_db
        self.panggilan_balik_sukses = panggilan_balik_sukses
        
        # konfigurasi grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, width=350, height=450, corner_radius=15)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.judul_apk()
        

    def judul_apk(self):
        self.label = ctk.CTkLabel(self, text="Aplikasi Kesehatan", 
                                       font=ctk.CTkFont(size=24, weight="bold", family="Inter"), text_color=THEME_GREEN)
        self.label.pack(pady=(40,20))

         # Segmented Button untuk beralih antara Login dan Daftar
        self.pemisah_tombol_var = ctk.StringVar(value="Login")
        self.pemisah_tombol = ctk.CTkSegmentedButton(self.main_frame, 
                                                       values=["Login", "Daftar"],
                                                       command=self.change_mode,
                                                       selected_color="#4CAF50", # Hijau
                                                       selected_hover_color="#388E3C",
                                                       variable=self.pemisah_tombol_var)
        self.pemisah_tombol.pack(pady=15, padx=30, fill="x")
    
        # Container untuk input (untuk memudahkan switch)
        self.frame_input = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_input.pack(pady=10, padx=20, fill="both", expand=True)
        self.frame_input.grid_columnconfigure(0, weight=1)

        self.buat_frame_daftar()
        self.buat_frame_masuk()
        
        # Tampilkan mode default (Login)
        self.tampilkan_frame_masuk()
        
    def buat_frame_masuk(self):
        """Membuat frame untuk fungsi Masuk."""
                         
        # Entri Nama Pengguna
        self.entri_nama_pengguna_masuk = ctk.CTkEntry(self.frame_input, placeholder_text="Nama Pengguna", width=250, corner_radius=8)
        self.entri_nama_pengguna_masuk.pack(pady=10)
        
        # Entri Kata Sandi
        self.entri_kata_sandi_masuk = ctk.CTkEntry(self.frame_input, placeholder_text="Kata Sandi", show="*", width=250, corner_radius=8)
        self.entri_kata_sandi_masuk.pack(pady=10)
        
        # Tombol Masuk
        self.tombol_masuk = ctk.CTkButton(self.frame_input, text="Masuk", command=self.masuk_pengguna, width=250, fg_color=THEME_BLUE, hover_color="#1565C0").pack(pady=15)
        
       
    def buat_frame_daftar(self):
        """Membuat frame untuk fungsi Daftar."""
              
        # Entri Nama Lengkap (Opsional)
        self.entri_nama_lengkap = ctk.CTkEntry(self.frame_input, placeholder_text="Nama Lengkap (Opsional)", width=250)
        self.entri_nama_lengkap.pack(pady=10)
        
        # Entri Nama Pengguna
        self.entri_nama_pengguna_daftar = ctk.CTkEntry(self.frame_input, placeholder_text="Nama Pengguna", width=250)
        self.entri_nama_pengguna_daftar.pack(pady=10)
        
        # Entri Kata Sandi
        self.entri_kata_sandi_daftar = ctk.CTkEntry(self.frame_input, placeholder_text="Kata Sandi", show="*", width=250)
        self.entri_kata_sandi_daftar.pack(pady=10)
        
        # Tombol Daftar
        self.tombol_daftar = ctk.CTkButton(self.frame_input, text="Daftar", command=self.daftar_pengguna, width=250, fg_color=THEME_GREEN, hover_color="#388E3C").pack(pady=15)
        
    def sembunyikan_semua_frame(self):
        """Menyembunyikan semua frame (Masuk dan Daftar)."""
        for widget in self.frame_input.winfo_children():
            widget.grid_forget()


    def tampilkan_frame_masuk(self):
        """Menampilkan frame masuk """
        self.sembunyikan_semua_frame()
        self.entri_nama_pengguna_masuk.grid(row=0, column=0, pady=10, padx=10)
        self.entri_kata_sandi_masuk.grid(row=1, column=0, pady=10, padx=10)
        self.tombol_masuk.grid(row=2, column=0, pady=20, padx=10)


    def tampilkan_frame_daftar(self):
        """Menampilkan frame daftar dan menyembunyikan frame masuk."""
        self.sembunyikan_semua_frame()
        self.entri_nama_lengkap.grid(row=0, column=0, pady=10, padx=10)
        self.entri_nama_pengguna_daftar.grid(row=1, column=0, pady=10, padx=10)
        self.entri_kata_sandi_daftar.grid(row=2, column=0, pady=10, padx=10)
        self.tombol_daftar.grid(row=3, column=0, pady=20, padx=10)

    def ganti_mode(self, nilai):
        """Mengganti antara tampilan Masuk dan Daftar."""
        if nilai == "Login":
            self.tampilkan_frame_masuk()
        else:
            self.tampilkan_frame_daftar()

    def masuk_pengguna(self):
        """Memproses otentikasi pengguna."""
        nama_pengguna = self.entri_nama_pengguna_masuk.get()
        kata_sandi = self.entri_kata_sandi_masuk.get()

        if not nama_pengguna or not kata_sandi:
            messagebox.showerror("Error", "Nama pengguna dan kata sandi harus diisi.")
            return

        data_pengguna = self.manajer_db.autentikasi_pengguna(nama_pengguna, kata_sandi)

        if data_pengguna:
            # Panggil panggilan balik sukses dengan ID dan peran pengguna
            id_pengguna = data_pengguna['id']
            messagebox.showinfo("Sukses", f"Selamat datang, {nama_pengguna}!")
            self.panggilan_balik_sukses(id_pengguna, data_pengguna['peran'])
        else:
            messagebox.showerror("Login Gagal!", "Nama pengguna atau kata sandi salah.")

    def daftar_pengguna(self):
        """Memproses pendaftaran pengguna baru."""
        nama_pengguna = self.entri_nama_pengguna_daftar.get()
        kata_sandi = self.entri_kata_sandi_daftar.get()
        konfirmasi_sandi = self.entri_konfirmasi_sandi_daftar.get()
        # Nama lengkap tidak digunakan saat mendaftar, akan diisi di profil
        
        self.label_kesalahan_daftar.configure(text="")

        if not nama_pengguna or not kata_sandi:
            messagebox.showerror("Error", "Nama pengguna dan kata sandi harus diisi.")
            return

        if self.manajer_db.tambah_pengguna(nama_pengguna, kata_sandi):
            messagebox.showinfo("Sukses", "Akun berhasil didaftarkan! Silakan masuk.")
            self.pemisah_tombol_var.set("Login")
            self.tampilkan_frame_masuk()
        else:
            messagebox.showerror("Nama pengguna sudah terdaftar.")
