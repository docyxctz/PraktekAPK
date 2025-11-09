import customtkinter as ctk
from manajer_basis_data import ManajerBasisData
from halaman_masuk_daftar import HalamanMasukDaftar
from dasbor_pengguna import DasborPengguna
from dasbor_admin import DasborAdmin

class Aplikasi(ctk.CTk):
    """Kelas utama aplikasi Health Tracker."""
    def __init__(self):
        super().__init__()
        
        # 🟢 Pengaturan Tema dan Tampilan Awal 🔵
        ctk.set_appearance_mode("Dark") # Tema gelap
        ctk.set_default_color_theme("green") # Menggunakan warna hijau/biru
        
        self.title("Aplikasi Kesehatan - Health Tracker")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # Konfigurasi agar frame mengisi seluruh window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Inisialisasi Basis Data
        self.basis_data = ManajerBasisData()
        
        # Tampilkan halaman Masuk/Daftar
        self.tampilkan_halaman_masuk()

    def tampilkan_halaman_masuk(self):
        """Menampilkan halaman Masuk/Daftar."""
        # Hapus frame yang ada
        for widget in self.winfo_children():
            widget.destroy()
            
        self.halaman_masuk = HalamanMasukDaftar(self, self.basis_data, self.tangani_sukses_masuk)
        self.halaman_masuk.grid(row=0, column=0, sticky="nsew")

    def tangani_sukses_masuk(self, id_pengguna, peran):
        """Dipanggil setelah masuk berhasil untuk menampilkan dasbor yang sesuai."""
        # Hapus frame masuk
        for widget in self.winfo_children():
            widget.destroy()
            
        if peran == 'admin':
            # Tampilkan Dasbor Admin
            self.dasbor = DasborAdmin(self, self.basis_data, id_pengguna)
            self.dasbor.grid(row=0, column=0, sticky="nsew")
        elif peran == 'user':
            # Tampilkan Dasbor Pengguna
            self.dasbor = DasborPengguna(self, self.basis_data, id_pengguna)
            self.dasbor.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    # Penting: Pastikan Anda telah menginstal customtkinter dan matplotlib
    # pip install customtkinter matplotlib

    app = Aplikasi()
    app.mainloop()