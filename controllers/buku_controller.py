from os import error
import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol simpan
        self.view.btn_simpan.configure(command=self.simpan_data)
        # Binding tombol update
        self.view.btn_update.configure(command=self.update_data)
        # Binding tombol delete
        self.view.btn_delete.configure(command=self.delete_data)

        # OTORISASI: Jika bukan admin, nonaktifkan form input dan tombol simpan
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def simpan_data(self):
        # Proteksi ganda di Level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def update_data(self):
        # Proteksi hak akses admin
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk memperbarui data!"
            )
            return

        # Memeriksa apakah ada buku yang dipilih
        pilihan = self.view.tabel.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku yang ingin diperbarui!"
            )
            return

        # Mengambil ID buku dari tabel
        data = self.view.tabel.item(pilihan[0], "values")
        id_buku = int(data[0])

        # Mengambil data dari form
        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        # Validasi form
        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!"
            )
            return

        # Validasi tahun terbit
        try:
            tahun = int(tahun)

            if tahun <= 0:
                messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus lebih dari 0!"
                )
                return

        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka!"
            )
            return

        try:
            # Memanggil fungsi update pada model
            success = self.model.update_buku(
                id_buku,
                judul,
                penulis,
                tahun
            )

            if success:
                messagebox.showinfo(
                    "Sukses",
                    "Data buku berhasil diperbarui!"
                )

                # Memperbarui tabel
                self.muat_data_tabel()

                # Membersihkan form
                self.view.entry_judul.delete(0, "end")
                self.view.entry_penulis.delete(0, "end")
                self.view.entry_tahun.delete(0, "end")

            else:
                messagebox.showerror(
                    "Gagal",
                    "Data buku gagal diperbarui!"
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Terjadi kesalahan saat memperbarui data:\n{error}"
            )
        

    def delete_data(self):
        # Proteksi hak akses admin
        if self.user_role != "admin":
            messagebox.showerror(
            "Akses Ditolak",
            "Anda tidak memiliki izin untuk menghapus data!"
        )
        return
    
        # Memeriksa apakah ada buku yang dipilih
        pilihan = self.view.tabel.selection()

        if not pilihan:
            messagebox.showwarning(
            "Peringatan",
            "Pilih data buku yang ingin dihapus!"
        )
        return

        # Mengambil ID buku dari baris yang dipilih
        data = self.view.tabel.item(pilihan[0], "values")
        id_buku = int(data[0])

        # Konfirmasi penghapusan
        konfirmasi = messagebox.askyesno(
        "Konfirmasi Hapus",
        "Apakah Anda yakin ingin menghapus buku ini?"
    )

        if not konfirmasi:
            return

        try:
            # Memanggil fungsi delete pada model
            success = self.model.delete_buku(id_buku)

            if success:
                messagebox.showinfo(
                "Sukses",
                "Data buku berhasil dihapus!"
                )

                # Memperbarui tabel setelah penghapusan
                self.muat_data_tabel()

                # Membersihkan form input
                self.view.entry_judul.delete(0, "end")
                self.view.entry_penulis.delete(0, "end")
                self.view.entry_tahun.delete(0, "end")

            else:
                messagebox.showwarning(
                "Peringatan",
                "Data buku gagal dihapus atau tidak ditemukan!"
                )

        except Exception as error:
            messagebox.showerror(
            "Gagal Menghapus",
            "Data buku tidak dapat dihapus.\n"
            "Buku mungkin masih tercatat dalam peminjaman.\n\n"
            f"Detail error: {error}"
            )

    def run(self):
        self.view.mainloop()