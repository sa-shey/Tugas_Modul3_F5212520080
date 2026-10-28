from tkinter import messagebox
from models.buku_model import BukuModel


class BukuController:
    def __init__(self, view):
        self.view = view
        self.model = BukuModel()

    def load_data(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        daftar_buku = self.model.get_all_buku()

        for buku in daftar_buku:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku["id_buku"],
                    buku["judul"],
                    buku["penulis"],
                    buku["tahun_terbit"]
                )
            )

    def pilih_data(self, event=None):
        pilihan = self.view.tabel.selection()

        if not pilihan:
            return

        data = self.view.tabel.item(pilihan[0], "values")

        self.view.entry_judul.delete(0, "end")
        self.view.entry_penulis.delete(0, "end")
        self.view.entry_tahun.delete(0, "end")

        self.view.entry_judul.insert(0, data[1])
        self.view.entry_penulis.insert(0, data[2])
        self.view.entry_tahun.insert(0, data[3])

    def update_data(self):
        pilihan = self.view.tabel.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih buku yang ingin diperbarui!"
            )
            return

        data = self.view.tabel.item(pilihan[0], "values")
        id_buku = int(data[0])

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!"
            )
            return

        try:
            tahun = int(tahun)

            berhasil = self.model.update_buku(
                id_buku, judul, penulis, tahun
            )

            if berhasil:
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

        except Exception as error:
            messagebox.showerror("Error", str(error))

    
    
    def delete_data(self):
        pilihan = self.view.tabel.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih buku yang ingin dihapus!"
            )
            return

        data = self.view.tabel.item(pilihan[0], "values")
        id_buku = int(data[0])

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus buku '{data[1]}'?"
        )

        if konfirmasi:
            try:
                berhasil = self.model.delete_buku(id_buku)

                if berhasil:
                    messagebox.showinfo(
                        "Sukses",
                        "Data buku berhasil dihapus!"
                    )
                    self.load_data()
                    self.view.bersihkan_form()

            except Exception as error:
                messagebox.showerror(
                    "Gagal",
                    "Data buku gagal dihapus.\n" + str(error)
                )

