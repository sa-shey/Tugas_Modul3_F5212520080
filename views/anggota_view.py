import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
from models.anggota_model import AnggotaModel
from controllers.anggota_controller import AnggotaController

class AnggotaView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Perpustakaan - Manajemen Data Anggota")
        self.geometry("900x520")
        self.controller = AnggotaController(self)

        # Inisialisasi Model Anggota
        self.anggota_model = AnggotaModel()

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # 1. FRAME KIRI: FORMULIR INPUT ANGGOTA
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Anggota", font=("Arial", 16, "bold")).pack(pady=15)

        # Nama Anggota
        ctk.CTkLabel(self.frame_kiri, text="Nama Anggota:", anchor="w").pack(fill="x", padx=15, pady=(5, 0))
        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Lengkap")
        self.entry_nama.pack(pady=5, padx=15, fill="x")

        # Alamat (Menggunakan CTkTextbox)
        ctk.CTkLabel(self.frame_kiri, text="Alamat:", anchor="w").pack(fill="x", padx=15, pady=(5, 0))
        self.text_alamat = ctk.CTkTextbox(self.frame_kiri, height=90)
        self.text_alamat.pack(pady=5, padx=15, fill="x")

        # Tombol Aksi (Simpan dihubungkan ke function simpan_data)
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="#28a745", hover_color="#218838", command=self.simpan_data)
        self.btn_simpan.pack(pady=(15, 5), padx=15, fill="x")

        self.btn_update = ctk.CTkButton(self.frame_kiri, text="Perbarui Data (Update)", fg_color="#1d6fa5", hover_color="#15527a")
        self.btn_update.pack(pady=5, padx=15, fill="x")

        self.btn_delete = ctk.CTkButton(self.frame_kiri, text="Hapus Data (Delete)", fg_color="#c82333", hover_color="#bd2130")
        self.btn_delete.pack(pady=5, padx=15, fill="x")

        # 2. FRAME KANAN: TABEL DAFTAR ANGGOTA
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Anggota Perpustakaan", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Tabel (Treeview)
        kolom = ("id", "nama", "alamat")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=16)

        self.tabel.heading("id", text="ID Anggota")
        self.tabel.heading("nama", text="Nama Anggota")
        self.tabel.heading("alamat", text="Alamat")

        self.tabel.column("id", width=80, anchor="center")
        self.tabel.column("nama", width=180)
        self.tabel.column("alamat", width=280)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

        # Memuat data awal saat aplikasi dibuka
        self.load_data()

    def load_data(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)
        data = self.anggota_model.get_all_anggota()
        for row in data:
            id_val = row.get("id_anggota") if "id_anggota" in row else row.get("id", "")
            self.tabel.insert("", "end", values=(id_val, row.get("nama"), row.get("alamat")))

    def simpan_data(self):
        nama = self.entry_nama.get()
        alamat = self.text_alamat.get("1.0", "end-1c").strip()

        if nama and alamat:
            success = self.anggota_model.create_anggota(nama, alamat)
            if success:
                messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
                self.load_data()  # Memperbarui jadual di sebelah kanan secara automatik
                self.entry_nama.delete(0, "end")
                self.text_alamat.delete("1.0", "end")
            else:
                messagebox.showerror("Error", "Gagal menyimpan data ke database.")
        else:
            messagebox.showwarning("Peringatan", "Nama dan Alamat tidak boleh kosong!")

if __name__ == "__main__":
    app = AnggotaView()
    app.mainloop()