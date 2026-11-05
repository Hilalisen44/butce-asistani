"""
Veri katmanı: Bütçe hedefi tablosu işlemleri.
"""
import sqlite3
from veri.veritabani import baglanti_al


def hedef_kaydet(kullanici_id, kategori_id, limit_tutar, ay):
    """Hedef yoksa ekler, varsa limitini günceller (UPSERT)."""
    baglanti = baglanti_al()
    try:
        baglanti.execute(
            """
            INSERT INTO butce_hedefi (kullanici_id, kategori_id, limit_tutar, ay)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(kullanici_id, kategori_id, ay)
            DO UPDATE SET limit_tutar = excluded.limit_tutar
            """,
            (kullanici_id, kategori_id, limit_tutar, ay),
        )
        baglanti.commit()
    except sqlite3.Error:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()


def hedefleri_listele(kullanici_id, ay):
    """O ayın hedeflerini, her birinde HARCANAN tutarla birlikte getirir."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute(
            """
            SELECT h.id, h.kategori_id, k.ad AS kategori, h.limit_tutar, h.ay,
                   COALESCE((
                       SELECT SUM(i.tutar) FROM islem i
                       WHERE i.kullanici_id = h.kullanici_id
                         AND i.kategori_id = h.kategori_id
                         AND substr(i.tarih, 1, 7) = h.ay
                   ), 0) AS harcanan
            FROM butce_hedefi h
            JOIN kategori k ON h.kategori_id = k.id
            WHERE h.kullanici_id = ? AND h.ay = ?
            ORDER BY k.ad
            """,
            (kullanici_id, ay),
        ).fetchall()
    finally:
        baglanti.close()


def hedef_sil(hedef_id, kullanici_id):
    """Sadece hedefin SAHİBİ silebilir. Silinen satır sayısını döndürür."""
    baglanti = baglanti_al()
    try:
        imlec = baglanti.execute(
            "DELETE FROM butce_hedefi WHERE id = ? AND kullanici_id = ?",
            (hedef_id, kullanici_id),
        )
        baglanti.commit()
        return imlec.rowcount
    except sqlite3.Error:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()