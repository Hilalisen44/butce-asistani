"""
Veri katmanı: İşlem (gelir/gider) tablosu için CRUD fonksiyonları.
C = Create (ekle), R = Read (oku), U = Update (güncelle), D = Delete (sil)
"""
import sqlite3
from veri.veritabani import baglanti_al


def islem_ekle(kullanici_id, kategori_id, tutar, tarih, aciklama=""):
    """C - Yeni işlem ekler ve eklenen kaydın id'sini döndürür."""
    baglanti = baglanti_al()
    try:
        imlec = baglanti.execute(
            "INSERT INTO islem (kullanici_id, kategori_id, tutar, tarih, aciklama) "
            "VALUES (?, ?, ?, ?, ?)",
            (kullanici_id, kategori_id, tutar, tarih, aciklama),
        )
        baglanti.commit()
        return imlec.lastrowid
    except sqlite3.Error:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()


def islemleri_listele(kullanici_id, kategori_id=None, arama=None, baslangic=None, bitis=None):
    """R - Kullanıcının işlemlerini, isteğe bağlı filtrelerle listeler."""
    sorgu = """
        SELECT islem.id, islem.tutar, islem.tarih, islem.aciklama,
               kategori.ad AS kategori, kategori.tur
        FROM islem
        JOIN kategori ON islem.kategori_id = kategori.id
        WHERE islem.kullanici_id = ?
    """
    parametreler = [kullanici_id]

    if kategori_id:
        sorgu += " AND islem.kategori_id = ?"
        parametreler.append(kategori_id)
    if arama:
        sorgu += " AND islem.aciklama LIKE ?"
        parametreler.append(f"%{arama}%")
    if baslangic:
        sorgu += " AND islem.tarih >= ?"
        parametreler.append(baslangic)
    if bitis:
        sorgu += " AND islem.tarih <= ?"
        parametreler.append(bitis)

    sorgu += " ORDER BY islem.tarih DESC, islem.id DESC"

    baglanti = baglanti_al()
    try:
        return baglanti.execute(sorgu, parametreler).fetchall()
    finally:
        baglanti.close()
        

def islem_getir(islem_id):
    """R - Tek bir işlemi id'sine göre getirir. Yoksa None döner."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute("SELECT * FROM islem WHERE id = ?", (islem_id,)).fetchone()
    finally:
        baglanti.close()


def tur_toplamlari(kullanici_id):
    """Kullanıcının toplam gelir ve giderini hesaplar."""
    baglanti = baglanti_al()
    try:
        satirlar = baglanti.execute(
            """
            SELECT kategori.tur, SUM(islem.tutar) AS toplam
            FROM islem
            JOIN kategori ON islem.kategori_id = kategori.id
            WHERE islem.kullanici_id = ?
            GROUP BY kategori.tur
            """,
            (kullanici_id,),
        ).fetchall()
        return {s["tur"]: s["toplam"] for s in satirlar}
    finally:
        baglanti.close()


def islem_guncelle(islem_id, kullanici_id, tutar, aciklama):
    """U - Sadece işlemin SAHİBİ güncelleyebilir."""
    baglanti = baglanti_al()
    try:
        imlec = baglanti.execute(
            "UPDATE islem SET tutar = ?, aciklama = ? WHERE id = ? AND kullanici_id = ?",
            (tutar, aciklama, islem_id, kullanici_id),
        )
        baglanti.commit()
        return imlec.rowcount
    except sqlite3.Error:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()


def islem_sil(islem_id, kullanici_id):
    """D - Sadece işlemin SAHİBİ silebilir."""
    baglanti = baglanti_al()
    try:
        imlec = baglanti.execute(
            "DELETE FROM islem WHERE id = ? AND kullanici_id = ?",
            (islem_id, kullanici_id),
        )
        baglanti.commit()
        return imlec.rowcount
    except sqlite3.Error:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()