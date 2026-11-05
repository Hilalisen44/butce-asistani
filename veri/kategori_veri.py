"""
Veri katmanı: Kategori tablosu işlemleri.
"""
from veri.veritabani import baglanti_al


def kategorileri_listele():
    """Tüm kategorileri türe ve ada göre sıralı getirir."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute("SELECT * FROM kategori ORDER BY tur, ad").fetchall()
    finally:
        baglanti.close()


def kategori_getir(kategori_id):
    """Tek bir kategoriyi getirir. Yoksa None döner."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute("SELECT * FROM kategori WHERE id = ?", (kategori_id,)).fetchone()
    finally:
        baglanti.close()