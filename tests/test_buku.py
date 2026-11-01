from models.buku_model import BukuModel


def test_get_all_buku():
    buku = BukuModel()

    try:
        hasil = buku.get_all_buku()

        # Memastikan hasil berupa list
        assert isinstance(hasil, list)

        # Memeriksa struktur setiap data buku
        for data in hasil:
            assert "id_buku" in data
            assert "judul" in data
            assert "penulis" in data
            assert "tahun_terbit" in data

    finally:
        if buku.conn:
            buku.conn.close()
