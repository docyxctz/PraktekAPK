import customtkinter as ctk
from tkinter import messagebox
from manajer_basis_data import ManajerBasisData

class LoginRegisterPage(ctk.CTkFrame):
    def __init__(self, master, db_manager: ManajerBasisData, success_callback):
        super().__init__(master)
        self.db = db_manager
        self.success_callback = success_callback
        
        # Grid konfigurasi agar frame login di tengah
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.main_frame = ctk.CTkFrame(self, width=350, height=450, corner_radius=15)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # Header
        self.label = ctk.CTkLabel(self.main_frame, text="APLIKASI KESEHATAN", 
                                  font=ctk.CTkFont(size=24, weight="bold", family="Inter"))
        self.label.pack(pady=(40, 10))
        
        # Segmented Button untuk beralih antara Login dan Daftar
        self.segmented_button_var = ctk.StringVar(value="Login")
        self.segmented_button = ctk.CTkSegmentedButton(self.main_frame, 
                                                       values=["Login", "Daftar"],
                                                       command=self.change_mode,
                                                       selected_color="#4CAF50", # Hijau
                                                       selected_hover_color="#388E3C",
                                                       variable=self.segmented_button_var)
        self.segmented_button.pack(pady=15, padx=30, fill="x")

        # Container untuk input (untuk memudahkan switch)
        self.input_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_container.pack(pady=10, padx=20, fill="both", expand=True)
        self.input_container.grid_columnconfigure(0, weight=1)

        self.create_login_widgets()
        self.create_register_widgets()
        
        # Tampilkan mode default (Login)
        self.show_login_widgets()

    def create_login_widgets(self):
        """Membuat widget untuk mode Login."""
        self.login_username_entry = ctk.CTkEntry(self.input_container, placeholder_text="Username", width=250, corner_radius=8)
        self.login_password_entry = ctk.CTkEntry(self.input_container, placeholder_text="Password", show="*", width=250, corner_radius=8)
        self.login_button = ctk.CTkButton(self.input_container, text="Login", command=self.handle_login, 
                                          fg_color="#1E88E5", hover_color="#1565C0", width=250) # Biru
        
    def create_register_widgets(self):
        """Membuat widget untuk mode Daftar."""
        self.register_username_entry = ctk.CTkEntry(self.input_container, placeholder_text="Username Baru", width=250, corner_radius=8)
        self.register_password_entry = ctk.CTkEntry(self.input_container, placeholder_text="Password", show="*", width=250, corner_radius=8)
        self.register_confirm_entry = ctk.CTkEntry(self.input_container, placeholder_text="Konfirmasi Password", show="*", width=250, corner_radius=8)
        self.register_button = ctk.CTkButton(self.input_container, text="Daftar Akun", command=self.handle_register,
                                            fg_color="#4CAF50", hover_color="#388E3C", width=250) # Hijau
        
    def hide_all_widgets(self):
        """Menyembunyikan semua widget input."""
        for widget in self.input_container.winfo_children():
            widget.grid_forget()

    def show_login_widgets(self):
        """Menampilkan widget Login."""
        self.hide_all_widgets()
        self.login_username_entry.grid(row=0, column=0, pady=10, padx=10)
        self.login_password_entry.grid(row=1, column=0, pady=10, padx=10)
        self.login_button.grid(row=2, column=0, pady=20, padx=10)

    def show_register_widgets(self):
        """Menampilkan widget Daftar."""
        self.hide_all_widgets()
        self.register_username_entry.grid(row=0, column=0, pady=10, padx=10)
        self.register_password_entry.grid(row=1, column=0, pady=10, padx=10)
        self.register_confirm_entry.grid(row=2, column=0, pady=10, padx=10)
        self.register_button.grid(row=3, column=0, pady=20, padx=10)

    def change_mode(self, value):
        """Mengganti antara tampilan Login dan Daftar."""
        if value == "Login":
            self.show_login_widgets()
        else:
            self.show_register_widgets()

    def handle_login(self):
        """Logika penanganan Login."""
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Login Gagal", "Username dan Password harus diisi.")
            return

        user_data = self.db.login_user(username, password)
        
        if user_data:
            user_id, role = user_data
            messagebox.showinfo("Login Sukses", f"Selamat datang, {username}! Role: {role.capitalize()}")
            self.success_callback(user_id, role) # Pindah ke dashboard
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah.")

    def handle_register(self):
        """Logika penanganan Daftar."""
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        confirm = self.register_confirm_entry.get()

        if not username or not password or not confirm:
            messagebox.showerror("Daftar Gagal", "Semua kolom harus diisi.")
            return

        if password != confirm:
            messagebox.showerror("Daftar Gagal", "Konfirmasi Password tidak cocok.")
            return
            
        if self.db.register_user(username, password, role='user'):
            messagebox.showinfo("Daftar Sukses", "Akun Pengguna berhasil dibuat! Silakan Login.")
            self.segmented_button_var.set("Login")
            self.show_login_widgets()
        else:
            messagebox.showerror("Daftar Gagal", "Username sudah terdaftar. Coba yang lain.")