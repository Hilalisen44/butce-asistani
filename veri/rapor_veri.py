"""
Veri katmanı: Panel ve yönetici ekranı için özet sorgular.
"""
import sqlite3
from veri.veritabani import baglanti_al


def kategori_harcamalari(kullanici_id, ay):
    """Bir kullanıcının o ayki giderlerini kategori kategori toplar."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute(
            """
            SELECT k.ad AS kategori, SUM(i.tutar) AS toplam
            FROM islem i
            JOIN kategori k ON i.kategori_id = k.id
            WHERE i.kullanici_id = ? AND k.tur = 'gider' AND substr(i.tarih, 1, 7) = ?
            GROUP BY k.ad
            ORDER BY toplam DESC
            """,
            (kullanici_id, ay),
        ).fetchall()
    finally:
        baglanti.close()


def genel_sayilar():
    """Sistemdeki toplam kullanıcı, işlem, kategori ve hedef sayısı."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute(
            """
            SELECT (SELECT COUNT(*) FROM kullanici)    AS kullanici,
                   (SELECT COUNT(*) FROM islem)        AS islem,
                   (SELECT COUNT(*) FROM kategori)     AS kategori,
                   (SELECT COUNT(*) FROM butce_hedefi) AS hedef
            """
        ).fetchone()
    finally:
        baglanti.close()


def kullanici_istatistikleri():
    """Her kullanıcının işlem sayısı ve toplam gideri. (Parola hash'i bilerek SEÇİLMİYOR.)"""
    baglanti = baglanti_al()
    try:
        return baglanti.execute(
            """
            SELECT u.id, u.ad, u.eposta, u.rol,
                   COUNT(i.id) AS islem_sayisi,
                   COALESCE(SUM(CASE WHEN k.tur = 'gider' THEN i.tutar END), 0) AS toplam_gider
            FROM kullanici u
            LEFT JOIN islem i    ON i.kullanici_id = u.id
            LEFT JOIN kategori k ON k.id = i.kategori_id
            GROUP BY u.id
            ORDER BY u.id
            """
        ).fetchall()
    finally:
        baglanti.close()


def kategori_kullanimi():
    """Her kategori ve içinde kaç işlem olduğu."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute(
            """
            SELECT k.id, k.ad, k.tur, COUNT(i.id) AS islem_sayisi
            FROM kategori k
            LEFT JOIN islem i ON i.kategori_id = k.id
            GROUP BY k.id
            ORDER BY k.tur, k.ad
            """
        ).fetchall()
    finally:
        baglanti.close()


def kategori_ekle(ad, tur):
    """Yeni kategori ekler."""
    baglanti = baglanti_al()
    try:
        baglanti.execute("INSERT INTO kategori (ad, tur) VALUES (?, ?)", (ad, tur))
        baglanti.commit()
    except sqlite3.Error:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()
