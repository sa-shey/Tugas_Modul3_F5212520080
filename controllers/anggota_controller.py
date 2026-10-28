
from tkinter import messagebox
from models.anggota_model import AnggotaModel


class AnggotaController:
    def __init__(self, view):
        self.view = view
        self.model = AnggotaModel()

    def load_data(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        daftar_anggota = self.model.get_all_anggota()

        for anggota in daftar_anggota:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    anggota["id_anggota"],
                    anggota["nama"],
                    anggota["alamat"]
                )
            )

    def simpan_data(self):
        nama = self.view.entry_nama.get().strip()
        alamat = self.view.entry_alamat.get().strip()

        if not nama or not alamat:
            messagebox.showwarning(
                "Peringatan",
                "Nama dan alamat harus diisi!"
            )
            return

        try:
            berhasil = self.model.create_anggota(nama, alamat)

            if berhasil:
                messagebox.showinfo(
                    "Sukses",
                    "Data anggota berhasil ditambahkan!"
                )

                self.view.entry_nama.delete(0, "end")
                self.view.entry_alamat.delete(0, "end")

                self.load_data()

        except Exception as error:
            messagebox.showerror(
                "Gagal",
                "Data anggota gagal ditambahkan.\n" + str(error)
            )
