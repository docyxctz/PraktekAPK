import customtkinter as ctk
from manajer_basis_data import ManajerBasisData
# Impor frame-frame konten dari file baru
from frame_dasbor_pengguna import FrameDasbor, FrameTarget, FrameInfo, FrameProfil

# Warna tema
THEME_GREEN = "#4CAF50"
THEME_BLUE = "#1E88E5"

class DasborPengguna(ctk.CTkFrame):
    def __init__(self, master, basis_data: ManajerBasisData, id_pengguna):
        super().__init__(master)
        self.basis_data = basis_data
        self.id_pengguna = id_pengguna
        
        # Konfigurasi Grid utama: Kolom 0 (Navigasi), Kolom 1 (Konten)
        self.grid_columnconfigure(0, weight=0) # Navigasi
        self.grid_columnconfigure(1, weight=1) # Konten
        self.grid_rowconfigure(0, weight=1)
        
        self.buat_frame_navigasi()
        self.buat_frame_konten_utama()
        
        # Mapping Frame
        self.peta_frame = {
            "Dasbor": FrameDasbor,
            "Target": FrameTarget,
            "Info": FrameInfo,
            "Profil": FrameProfil
        }
        
        self.frame_saat_ini = None
        self.tampilkan_frame("Dasbor")

    def buat_frame_navigasi(self):
        """Membuat Frame Navigasi (kiri)."""
        self.frame_nav = ctk.CTkFrame(self, width=180, corner_radius=0, fg_color="#1c1c1c")
        self.frame_nav.grid(row=0, column=0, sticky="nsew")
        self.frame_nav.grid_rowconfigure(5, weight=1) 
        
        self.label_logo = ctk.CTkLabel(self.frame_nav, text="Health Tracker", 
                                       font=ctk.CTkFont(size=20, weight="bold", slant="italic"), text_color=THEME_GREEN)
        self.label_logo.grid(row=0, column=0, padx=20, pady=20)
        
        # Tombol Navigasi
        nama_tombol = ["Dasbor", "Target", "Info", "Profil"]
        for i, nama in enumerate(nama_tombol):
            tombol = ctk.CTkButton(self.frame_nav, text=nama, command=lambda n=nama: self.tampilkan_frame(n),
                                   fg_color="transparent", hover_color="#2e2e2e", 
                                   text_color="white", anchor="w", corner_radius=5)
            tombol.grid(row=i+1, column=0, sticky="ew", padx=10, pady=5)
            setattr(self, f"tombol_{nama.lower()}", tombol)

        # Tombol Keluar
        self.tombol_keluar = ctk.CTkButton(self.frame_nav, text="Keluar", command=self.master.tampilkan_halaman_masuk,
                                           fg_color="#D32F2F", hover_color="#B71C1C")
        self.tombol_keluar.grid(row=6, column=0, sticky="s", padx=20, pady=20)

    def buat_frame_konten_utama(self):
        """Membuat Frame Konten Utama (kanan)."""
        self.wadah_konten_utama = ctk.CTkFrame(self, fg_color="transparent")
        self.wadah_konten_utama.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.wadah_konten_utama.grid_columnconfigure(0, weight=1)
        self.wadah_konten_utama.grid_rowconfigure(0, weight=1)

    def tampilkan_frame(self, nama_frame):
        """Menampilkan Frame yang dipilih dan menyembunyikan yang lain."""
        # Hapus frame yang sedang ditampilkan
        if self.frame_saat_ini:
            self.frame_saat_ini.destroy()

        kelas_frame = self.peta_frame.get(nama_frame)
        if kelas_frame:
            # Buat instance frame baru, melewatinya (master, db, id_pengguna)
            self.frame_saat_ini = kelas_frame(self.wadah_konten_utama, self.basis_data, self.id_pengguna)
            self.frame_saat_ini.grid(row=0, column=0, sticky="nsew")