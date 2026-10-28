from models.buku_model import BukuModel
from models.anggota_model import AnggotaModel
buku = BukuModel()

print("=== Update Data Buku ===")
if buku.update_buku(12, "Laut Bercerita", "Leila S. Chudori", 2019):
    print("Data buku berhasil diupdate!")

print()
print("=== Data Buku Setelah Update ===")
daftar_buku = buku.get_all_buku()

for data in daftar_buku:
    print(
        "[" + str(data["id_buku"]) + "]",
        data["judul"],
        "-",
        data["penulis"],
        "(" + str(data["tahun_terbit"]) + ")"
    )


print()
print("=== Delete Data Buku ===")

if buku.delete_buku(4):
    print("Data buku berhasil dihapus!")


print()
print("=== Data Buku Setelah Delete ===")
daftar_buku = buku.get_all_buku()

for data in daftar_buku:
    print(
        "[" + str(data["id_buku"]) + "]",
        data["judul"],
        "-",
        data["penulis"],
        "(" + str(data["tahun_terbit"]) + ")"
    )


print()
print("=== Create Data Anggota ===")
anggota = AnggotaModel()

if anggota.create_anggota("Dimas", "Jl. Merdeka"):
    print("Data anggota berhasil ditambahkan!")


print()
print("=== Data Anggota ===")
daftar_anggota = anggota.get_all_anggota()

for data in daftar_anggota:
    print(
        "[" + str(data["id_anggota"]) + "]",
        data["nama"],
        "-",
        data["alamat"]
    )

