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
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.buat_frame_masuk()
        self.buat_frame_daftar()
        
        self.tampilkan_frame_masuk()

    def buat_frame_masuk(self):
        """Membuat frame untuk fungsi Masuk."""
        self.frame_masuk = ctk.CTkFrame(self, corner_radius=10)
        
        ctk.CTkLabel(self.frame_masuk, text="Masuk Akun", 
                     font=ctk.CTkFont(size=24, weight="bold"), text_color=THEME_GREEN).pack(pady=20)
        
        # Entri Nama Pengguna
        self.entri_nama_pengguna_masuk = ctk.CTkEntry(self.frame_masuk, placeholder_text="Nama Pengguna", width=250)
        self.entri_nama_pengguna_masuk.pack(pady=10)
        
        # Entri Kata Sandi
        self.entri_kata_sandi_masuk = ctk.CTkEntry(self.frame_masuk, placeholder_text="Kata Sandi", show="*", width=250)
        self.entri_kata_sandi_masuk.pack(pady=10)
        
        # Tombol Masuk
        ctk.CTkButton(self.frame_masuk, text="Masuk", command=self.masuk_pengguna, width=250, fg_color=THEME_BLUE, hover_color="#1565C0").pack(pady=15)
        
        # Tombol Pindah ke Daftar
        ctk.CTkButton(self.frame_masuk, text="Belum punya akun? Daftar", command=self.tampilkan_frame_daftar,
                      fg_color="transparent", text_color="gray", hover_color="#2e2e2e").pack(pady=10)
        
        self.label_kesalahan_masuk = ctk.CTkLabel(self.frame_masuk, text="", text_color="#D32F2F")
        self.label_kesalahan_masuk.pack()

    def buat_frame_daftar(self):
        """Membuat frame untuk fungsi Daftar."""
        self.frame_daftar = ctk.CTkFrame(self, corner_radius=10)
        
        ctk.CTkLabel(self.frame_daftar, text="Daftar Akun Baru", 
                     font=ctk.CTkFont(size=24, weight="bold"), text_color=THEME_GREEN).pack(pady=20)
        
        # Entri Nama Lengkap (Opsional)
        self.entri_nama_lengkap = ctk.CTkEntry(self.frame_daftar, placeholder_text="Nama Lengkap (Opsional)", width=250)
        self.entri_nama_lengkap.pack(pady=10)
        
        # Entri Nama Pengguna
        self.entri_nama_pengguna_daftar = ctk.CTkEntry(self.frame_daftar, placeholder_text="Nama Pengguna", width=250)
        self.entri_nama_pengguna_daftar.pack(pady=10)
        
        # Entri Kata Sandi
        self.entri_kata_sandi_daftar = ctk.CTkEntry(self.frame_daftar, placeholder_text="Kata Sandi", show="*", width=250)
        self.entri_kata_sandi_daftar.pack(pady=10)
        
        # Tombol Daftar
        ctk.CTkButton(self.frame_daftar, text="Daftar", command=self.daftar_pengguna, width=250, fg_color=THEME_GREEN, hover_color="#388E3C").pack(pady=15)
        
        # Tombol Pindah ke Masuk
        ctk.CTkButton(self.frame_daftar, text="Sudah punya akun? Masuk", command=self.tampilkan_frame_masuk,
                      fg_color="transparent", text_color="gray", hover_color="#2e2e2e").pack(pady=10)
        
        self.label_kesalahan_daftar = ctk.CTkLabel(self.frame_daftar, text="", text_color="#D32F2F")
        self.label_kesalahan_daftar.pack()

    def tampilkan_frame_masuk(self):
        """Menampilkan frame masuk dan menyembunyikan frame daftar."""
        self.frame_daftar.grid_forget()
        self.frame_masuk.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.label_kesalahan_daftar.configure(text="")

    def tampilkan_frame_daftar(self):
        """Menampilkan frame daftar dan menyembunyikan frame masuk."""
        self.frame_masuk.grid_forget()
        self.frame_daftar.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.label_kesalahan_masuk.configure(text="")

    def masuk_pengguna(self):
        """Memproses otentikasi pengguna."""
        nama_pengguna = self.entri_nama_pengguna_masuk.get()
        kata_sandi = self.entri_kata_sandi_masuk.get()
        self.label_kesalahan_masuk.configure(text="")

        if not nama_pengguna or not kata_sandi:
            self.label_kesalahan_masuk.configure(text="Nama pengguna dan kata sandi harus diisi.")
            return

        hasil = self.manajer_db.autentikasi_pengguna(nama_pengguna, kata_sandi)

        if hasil:
            # Panggil panggilan balik sukses dengan ID dan peran pengguna
            self.panggilan_balik_sukses(hasil['id'], hasil['role'])
        else:
            self.label_kesalahan_masuk.configure(text="Nama pengguna atau kata sandi salah.")

    def daftar_pengguna(self):
        """Memproses pendaftaran pengguna baru."""
        nama_pengguna = self.entri_nama_pengguna_daftar.get()
        kata_sandi = self.entri_kata_sandi_daftar.get()
        # Nama lengkap tidak digunakan saat mendaftar, akan diisi di profil
        
        self.label_kesalahan_daftar.configure(text="")

        if not nama_pengguna or not kata_sandi:
            self.label_kesalahan_daftar.configure(text="Nama pengguna dan kata sandi harus diisi.")
            return

        if self.manajer_db.tambah_pengguna(nama_pengguna, kata_sandi):
            messagebox.showinfo("Sukses", "Akun berhasil didaftarkan! Silakan masuk.")
            self.tampilkan_frame_masuk()
        else:
            self.label_kesalahan_daftar.configure(text="Nama pengguna sudah digunakan.")