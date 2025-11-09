import customtkinter as ctk
from tkinter import messagebox
from manajer_basis_data import ManajerBasisData

# Warna tema
THEME_GREEN = "#4CAF50"
THEME_BLUE = "#1E88E5"

# --- EDITOR NUTRITION (Admin) ---
class EditorGizi(ctk.CTkFrame):
    def __init__(self, master, manajer_db: ManajerBasisData):
        super().__init__(master, corner_radius=10)
        self.manajer_db = manajer_db
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text="Edit Daftar Nilai Gizi Makanan", font=ctk.CTkFont(size=18, weight="bold"), text_color=THEME_GREEN).pack(pady=10)

        # Form Input
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(pady=5, padx=20)
        
        self.entri_nama = ctk.CTkEntry(form, placeholder_text="Nama Makanan", width=150)
        self.entri_nama.grid(row=0, column=0, padx=5, pady=5)
        self.entri_kal = ctk.CTkEntry(form, placeholder_text="Kalori (kcal)", width=100)
        self.entri_kal.grid(row=0, column=1, padx=5, pady=5)
        self.entri_prot = ctk.CTkEntry(form, placeholder_text="Protein (g)", width=100)
        self.entri_prot.grid(row=0, column=2, padx=5, pady=5)
        self.entri_lemak = ctk.CTkEntry(form, placeholder_text="Lemak (g)", width=100)
        self.entri_lemak.grid(row=1, column=0, padx=5, pady=5)
        self.entri_karbo = ctk.CTkEntry(form, placeholder_text="Karbo (g)", width=100)
        self.entri_karbo.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkButton(form, text="Simpan/Update", command=self.simpan_gizi, fg_color=THEME_BLUE, hover_color="#1565C0").grid(row=1, column=2, padx=5, pady=5)
        
        # Daftar Tampilan
        self.daftar_tampilan = ctk.CTkScrollableFrame(self, label_text="Data Gizi Tersimpan", width=550, height=250)
        self.daftar_tampilan.pack(padx=20, pady=10)
        self.muat_ulang_daftar()
        
    def simpan_gizi(self):
        try:
            nama = self.entri_nama.get()
            kalori = float(self.entri_kal.get())
            protein = float(self.entri_prot.get())
            lemak = float(self.entri_lemak.get())
            karbo = float(self.entri_karbo.get())
            
            if not nama:
                raise ValueError("Nama harus diisi.")

            self.manajer_db.update_gizi(nama, kalori, protein, lemak, karbo)
            messagebox.showinfo("Sukses", f"Data gizi '{nama}' berhasil diperbarui.")
            # Bersihkan input setelah sukses
            self.entri_nama.delete(0, 'end')
            self.entri_kal.delete(0, 'end')
            self.entri_prot.delete(0, 'end')
            self.entri_lemak.delete(0, 'end')
            self.entri_karbo.delete(0, 'end')
            
            self.muat_ulang_daftar()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Input tidak valid: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Kesalahan DB: {e}")

    def muat_ulang_daftar(self):
        # Bersihkan frame
        for widget in self.daftar_tampilan.winfo_children():
            widget.destroy()

        data = self.manajer_db.dapatkan_daftar_gizi()
        
        # Header Tabel
        header = ["Nama", "Kalori", "Protein", "Lemak", "Karbo"]
        for i, h in enumerate(header):
            ctk.CTkLabel(self.daftar_tampilan, text=h, font=ctk.CTkFont(weight="bold"), text_color=THEME_GREEN).grid(row=0, column=i, padx=5, pady=5)
            
        # Isi Tabel
        for indeks_baris, item in enumerate(data):
            ctk.CTkLabel(self.daftar_tampilan, text=item['name'], justify="left").grid(row=indeks_baris+1, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.daftar_tampilan, text=f"{item['calories']:.0f}").grid(row=indeks_baris+1, column=1, padx=5, pady=2)
            ctk.CTkLabel(self.daftar_tampilan, text=f"{item['protein']:.1f}g").grid(row=indeks_baris+1, column=2, padx=5, pady=2)
            ctk.CTkLabel(self.daftar_tampilan, text=f"{item['fat']:.1f}g").grid(row=indeks_baris+1, column=3, padx=5, pady=2)
            ctk.CTkLabel(self.daftar_tampilan, text=f"{item['carbs']:.1f}g").grid(row=indeks_baris+1, column=4, padx=5, pady=2)


# --- EDITOR EXERCISE (Admin) ---
class EditorLatihan(ctk.CTkFrame):
    def __init__(self, master, manajer_db: ManajerBasisData):
        super().__init__(master, corner_radius=10)
        self.manajer_db = manajer_db
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text="Edit Daftar Latihan", font=ctk.CTkFont(size=18, weight="bold"), text_color=THEME_GREEN).pack(pady=10)

        # Form Input
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(pady=5, padx=20)
        
        self.entri_nama = ctk.CTkEntry(form, placeholder_text="Nama Latihan", width=150)
        self.entri_nama.grid(row=0, column=0, padx=5, pady=5)
        self.entri_bakar_kal = ctk.CTkEntry(form, placeholder_text="Kalori Terbakar/Jam", width=150)
        self.entri_bakar_kal.grid(row=0, column=1, padx=5, pady=5)
        self.entri_deskripsi = ctk.CTkEntry(form, placeholder_text="Deskripsi Singkat", width=300)
        self.entri_deskripsi.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        ctk.CTkButton(form, text="Simpan/Update", command=self.simpan_latihan, fg_color=THEME_BLUE, hover_color="#1565C0").grid(row=2, column=0, columnspan=2, pady=10)
        
        # Daftar Tampilan
        self.daftar_tampilan = ctk.CTkScrollableFrame(self, label_text="Data Latihan Tersimpan", width=550, height=250)
        self.daftar_tampilan.pack(padx=20, pady=10)
        self.muat_ulang_daftar()
        
    def simpan_latihan(self):
        try:
            nama = self.entri_nama.get()
            kalori_terbakar = float(self.entri_bakar_kal.get())
            deskripsi = self.entri_deskripsi.get()
            
            if not nama or not deskripsi:
                raise ValueError("Nama dan Deskripsi harus diisi.")

            self.manajer_db.update_latihan(nama, kalori_terbakar, deskripsi)
            messagebox.showinfo("Sukses", f"Data latihan '{nama}' berhasil diperbarui.")
            # Bersihkan input setelah sukses
            self.entri_nama.delete(0, 'end')
            self.entri_bakar_kal.delete(0, 'end')
            self.entri_deskripsi.delete(0, 'end')
            
            self.muat_ulang_daftar()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Input tidak valid: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Kesalahan DB: {e}")

    def muat_ulang_daftar(self):
        # Bersihkan frame
        for widget in self.daftar_tampilan.winfo_children():
            widget.destroy()

        data = self.manajer_db.dapatkan_daftar_latihan()
        
        # Header Tabel
        ctk.CTkLabel(self.daftar_tampilan, text="Nama Latihan", font=ctk.CTkFont(weight="bold"), text_color=THEME_GREEN).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.daftar_tampilan, text="Kalori/Jam", font=ctk.CTkFont(weight="bold"), text_color=THEME_GREEN).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.daftar_tampilan, text="Deskripsi", font=ctk.CTkFont(weight="bold"), text_color=THEME_GREEN).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Isi Tabel
        for indeks_baris, item in enumerate(data):
            ctk.CTkLabel(self.daftar_tampilan, text=item['name'], justify="left").grid(row=indeks_baris+1, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.daftar_tampilan, text=f"{item['calories_burned_per_hour']:.0f}").grid(row=indeks_baris+1, column=1, padx=5, pady=2)
            ctk.CTkLabel(self.daftar_tampilan, text=item['description'], wraplength=200, justify="left").grid(row=indeks_baris+1, column=2, padx=5, pady=2, sticky="w")