import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
from models.buku_model import BukuModel
from controllers.buku_controller import BukuController

class BukuView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Perpustakaan - Manajemen Data Buku")
        self.geometry("900x520")
        self.controller = BukuController(self)

        # Inisialisasi Model Buku
        self.buku_model = BukuModel()

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # 1. FRAME KIRI: FORMULIR INPUT BUKU
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Input Buku", font=("Arial", 16, "bold")).pack(pady=15)

        # Judul Buku
        ctk.CTkLabel(self.frame_kiri, text="Judul Buku:", anchor="w").pack(fill="x", padx=15, pady=(5, 0))
        self.entry_judul = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Judul Buku")
        self.entry_judul.pack(pady=5, padx=15, fill="x")

        # Penulis
        ctk.CTkLabel(self.frame_kiri, text="Penulis:", anchor="w").pack(fill="x", padx=15, pady=(5, 0))
        self.entry_penulis = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Penulis")
        self.entry_penulis.pack(pady=5, padx=15, fill="x")

        # Tahun Terbit
        ctk.CTkLabel(self.frame_kiri, text="Tahun Terbit:", anchor="w").pack(fill="x", padx=15, pady=(5, 0))
        self.entry_tahun = ctk.CTkEntry(self.frame_kiri, placeholder_text="Contoh: 2024")
        self.entry_tahun.pack(pady=5, padx=15, fill="x")

        # Tombol Aksi (Simpan dihubungkan ke function simpan_data)
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="#28a745", hover_color="#218838", command=self.simpan_data)
        self.btn_simpan.pack(pady=(15, 5), padx=15, fill="x")

        
        # Tombol Perbarui Data (Update)
        self.btn_update = ctk.CTkButton(self.frame_kiri, text="Perbarui Data (Update)", fg_color="#1d6fa5", hover_color="#15527a", command=self.controller.update_data)
        self.btn_update.pack(fill="x", padx=10, pady=5)

        # Tombol Hapus Data (Delete)
        self.btn_delete = ctk.CTkButton( self.frame_kiri, text="Hapus Data (Delete)", fg_color="#c82333", hover_color="#bd2130", command=self.controller.delete_data)
        self.btn_delete.pack(fill="x", padx=10, pady=5)

        # 2. FRAME KANAN: TABEL DAFTAR BUKU
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Koleksi Buku", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Tabel (Treeview)
        kolom = ("id", "judul", "penulis", "tahun")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=16)

        self.tabel.heading("id", text="ID Buku")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun", text="Tahun Terbit")

        self.tabel.column("id", width=70, anchor="center")
        self.tabel.column("judul", width=220)
        self.tabel.column("penulis", width=150)
        self.tabel.column("tahun", width=90, anchor="center")

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)
        self.tabel.bind("<<TreeviewSelect>>", self.controller.pilih_data)

        # Memuat data awal saat aplikasi dibuka
        self.load_data()

    def load_data(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)
        data = self.buku_model.get_all_buku()
        for row in data:
            id_val = row.get("id_buku") if "id_buku" in row else row.get("id", "")
            self.tabel.insert("", "end", values=(id_val, row.get("judul"), row.get("penulis"), row.get("tahun_terbit")))

    def simpan_data(self):
        judul = self.entry_judul.get()
        penulis = self.entry_penulis.get()
        tahun = self.entry_tahun.get()

        if judul and penulis and tahun:
            success = self.buku_model.create_buku(judul, penulis, tahun)
            if success:
                messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
                self.load_data()  # Langsung memperbarui tabel di sebelah kanan
                self.entry_judul.delete(0, "end")
                self.entry_penulis.delete(0, "end")
                self.entry_tahun.delete(0, "end")
            else:
                messagebox.showerror("Error", "Gagal menyimpan data ke database.")
        else:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")


    def pilih_data(self, event=None):
        pilihan = self.tabel.selection()

        if pilihan:
            data = self.tabel.item(pilihan[0], "values")

            self.entry_judul.delete(0, "end")
            self.entry_penulis.delete(0, "end")
            self.entry_tahun.delete(0, "end")

            self.entry_judul.insert(0, data[1])
            self.entry_penulis.insert(0, data[2])
            self.entry_tahun.insert(0, data[3])

    def update_data(self):
        pilihan = self.tabel.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku yang ingin diperbarui!"
            )
            return

        data = self.tabel.item(pilihan[0], "values")
        id_buku = int(data[0])

        judul = self.entry_judul.get().strip()
        penulis = self.entry_penulis.get().strip()
        tahun = self.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!"
            )
            return

        try:
            tahun = int(tahun)

            success = self.buku_model.update_buku(
                id_buku, judul, penulis, tahun
            )

            if success:
                messagebox.showinfo(
                    "Sukses",
                    "Data buku berhasil diperbarui!"
                )
                self.load_data()

        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka!"
            )

    def delete_data(self):
        pilihan = self.tabel.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku yang ingin dihapus!"
            )
            return

        data = self.tabel.item(pilihan[0], "values")
        id_buku = int(data[0])

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Apakah Anda yakin ingin menghapus buku ini?"
        )

        if konfirmasi:
            try:
                success = self.buku_model.delete_buku(id_buku)

                if success:
                    messagebox.showinfo(
                        "Sukses",
                        "Data buku berhasil dihapus!"
                    )
                    self.load_data()

            except Exception as error:
                messagebox.showerror(
                    "Gagal Menghapus",
                    "Data buku tidak dapat dihapus.\n"
                    "Buku mungkin masih tercatat dalam peminjaman.\n"
                    + str(error)
                )

    def bersihkan_form(self):
        self.entry_judul.delete(0, "end")
        self.entry_penulis.delete(0, "end")
        self.entry_tahun.delete(0, "end")

        # Menghilangkan pilihan baris pada tabel
        self.tabel.selection_remove(self.tabel.selection())



if __name__ == "__main__":
    app = BukuView()
    app.mainloop()