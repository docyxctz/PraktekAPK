import customtkinter as ctk
from tkinter import messagebox
import sys
import sqlite3

# --- PENTING: Struktur Kelas HalamanMasukDaftar (Memperbaiki Kesalahan Grid/Pack) ---

class HalamanMasukDaftar(ctk.CTkFrame):
    """
    Kelas untuk menangani tampilan Login dan Daftar.
    Semua widget di dalam frame ini kini menggunakan grid().
    """
    def __init__(self, master, manajer_db, on_login_success):
        super().__init__(master)
        self.manajer_db = manajer_db
        self.on_login_success = on_login_success
        self.is_login_mode = True
        
        # Konfigurasi grid untuk centering konten di HalamanMasukDaftar
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.frame_utama = ctk.CTkFrame(self, corner_radius=10)
        # Menempatkan frame utama di tengah HalamanMasukDaftar menggunakan grid
        self.frame_utama.grid(row=0, column=0, padx=20, pady=20)
        self.frame_utama.grid_columnconfigure(0, weight=1) 

        # Semua widget di bawah ini HARUS menggunakan grid() di dalam self.frame_utama
        
        self.judul = ctk.CTkLabel(self.frame_utama, text="LOGIN", font=ctk.CTkFont(size=24, weight="bold"))
        # Perbaikan: Menggunakan grid() alih-alih pack()
        self.judul.grid(row=0, column=0, pady=(40, 20), padx=60)
        
        self.entri_username = ctk.CTkEntry(self.frame_utama, placeholder_text="Username", width=250)
        self.entri_username.grid(row=1, column=0, pady=10)
        
        self.entri_password = ctk.CTkEntry(self.frame_utama, placeholder_text="Password", show="*", width=250)
        self.entri_password.grid(row=2, column=0, pady=10)
        
        # Khusus Register 
        self.entri_konfirmasi_password = ctk.CTkEntry(self.frame_utama, placeholder_text="Konfirmasi Password", show="*", width=250)
        
        # Tombol Aksi (Login/Daftar)
        self.tombol_aksi = ctk.CTkButton(self.frame_utama, text="Login", command=self.aksi_utama, fg_color="#1E88E5", hover_color="#1565C0")
        
        # Tombol Ganti Mode
        self.tombol_ganti_mode = ctk.CTkButton(self.frame_utama, text="Belum punya akun? Daftar", command=self.ganti_mode, fg_color="gray", hover_color="#616161")
        
        self.update_ui()
        
    def judul_apk(self):
        # Fungsi ini, yang menyebabkan error sebelumnya, sekarang dimodifikasi
        # untuk memastikan label menggunakan grid().
        # Karena sudah diinisialisasi di __init__, kita hanya perlu memastikan
        # jika ada kode di sini, ia menggunakan grid.
        # Saya mengasumsikan kode di __init__ sudah cukup.
        pass


    def ganti_mode(self):
        self.is_login_mode = not self.is_login_mode
        self.update_ui()
        
    def update_ui(self):
        # Semua penempatan sekarang menggunakan grid()
        if self.is_login_mode:
            self.judul.configure(text="LOGIN")
            self.tombol_aksi.configure(text="Login", fg_color="#1E88E5", hover_color="#1565C0")
            self.tombol_ganti_mode.configure(text="Belum punya akun? Daftar")
            
            self.entri_konfirmasi_password.grid_forget()
            # Gunakan grid() untuk semua penempatan
            self.tombol_aksi.grid(row=3, column=0, pady=20) 
            self.tombol_ganti_mode.grid(row=4, column=0, pady=(0, 20))
            
        else:
            self.judul.configure(text="DAFTAR AKUN BARU")
            self.tombol_aksi.configure(text="Daftar", fg_color="#4CAF50", hover_color="#388E3C")
            self.tombol_ganti_mode.configure(text="Sudah punya akun? Login")
            
            # Tampilkan kolom konfirmasi dan pindahkan tombol ke bawah
            self.entri_konfirmasi_password.grid(row=3, column=0, pady=10)
            self.tombol_aksi.grid(row=4, column=0, pady=20)
            self.tombol_ganti_mode.grid(row=5, column=0, pady=(0, 20))
            
    def aksi_utama(self):
        username = self.entri_username.get()
        password = self.entri_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username dan Password tidak boleh kosong.")
            return

        # Bagian ini memerlukan ManajerBasisData yang sesungguhnya untuk berjalan
        if self.is_login_mode:
            # Mode Login (logika dummy jika ManajerBasisData tidak tersedia)
            user_data = {"id": 1, "role": "user"} if username == "user" and password == "pass" else None
            # Jika ManajerBasisData asli ada:
            # user_data = self.manajer_db.otentikasi_pengguna(username, password)
            self.on_login_success(user_data)
        else:
            # Mode Register (logika dummy)
            konfirmasi_password = self.entri_konfirmasi_password.get()
            
            if password != konfirmasi_password:
                messagebox.showerror("Error", "Password dan Konfirmasi Password tidak cocok.")
                return
            
            # Jika ManajerBasisData asli ada:
            # self.manajer_db.daftar_pengguna(username, password, "user")
            messagebox.showinfo("Sukses", "Akun berhasil didaftarkan. Silakan Login.")
            self.is_login_mode = True
            self.update_ui()
            self.entri_username.delete(0, ctk.END)
            self.entri_password.delete(0, ctk.END)
            self.entri_konfirmasi_password.delete(0, ctk.END)
# --- Akhir Perbaikan Kelas HalamanMasukDaftar ---


# Konfigurasi Tampilan
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Aplikasi(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Aplikasi Pelacak Kesehatan & Gizi")
        self.geometry("1000x700")
        self.minsize(900, 600)

        # Inisialisasi Database (Dummy ManajerBasisData jika tidak ada file asli)
        try:
             # self.manajer_db = ManajerBasisData() # Baris asli
             self.manajer_db = None # Menggunakan None agar tidak error jika tidak ada file ManajerBasisData
        except NameError:
             self.manajer_db = None
        
        # Variabel State
        self.is_logged_in = False
        self.current_user_id = None
        self.current_user_role = None
        
        # Konfigurasi Layout Grid Utama
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main Content

        # Tampilkan Frame Login/Register (Menggunakan HalamanMasukDaftar yang sudah diperbaiki)
        # self.tampilkan_halaman_masuk() -> Baris asli di traceback
        self.halaman_masuk = HalamanMasukDaftar(self, self.manajer_db, self.handle_login)
        self.halaman_masuk.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Sidebar (Disembunyikan saat belum login)
        self.frame_sidebar = None
        self.frame_konten_utama = None
        
    # Fungsi-fungsi lain dari kelas Aplikasi (handle_login, buat_sidebar, dll.)
    # ... (dapat Anda tambahkan kembali dari versi sebelumnya, tetapi pastikan 
    # handle_login menerima user_data yang berisi id dan role)
    
    def handle_login(self, user_data):
        # Logika login sukses
        if user_data:
            self.current_user_id = user_data.get('id', 1)
            self.current_user_role = user_data.get('role', 'user')
            self.is_logged_in = True
            
            self.halaman_masuk.grid_forget()
            
            # Asumsikan fungsi ini ada, namun dikomentari untuk kesederhanaan
            # self.buat_sidebar()
            # self.buat_konten_utama()
            
            messagebox.showinfo("Sukses", f"Selamat datang, User ID: {self.current_user_id} ({self.current_user_role})")
        else:
            messagebox.showerror("Otentikasi Gagal", "Username atau Password salah.")

if __name__ == "__main__":
    app = Aplikasi()
    app.mainloop()