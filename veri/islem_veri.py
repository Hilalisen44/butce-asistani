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
        baglanti.commit()          # her şey yolundaysa kaydet
        return imlec.lastrowid
    except sqlite3.Error:
        baglanti.rollback()        # hata olursa yarım kalan işlemi geri al
        raise                      # hatayı çağıran koda ilet
    finally:
        baglanti.close()           # HER DURUMDA bağlantıyı kapat


def islemleri_listele(kullanici_id):
    """R - Bir kullanıcının işlemlerini kategori adıyla birlikte, yeniden eskiye listeler."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute(
            """
            SELECT islem.id, islem.tutar, islem.tarih, islem.aciklama,
                   kategori.ad AS kategori, kategori.tur
            FROM islem
            JOIN kategori ON islem.kategori_id = kategori.id
            WHERE islem.kullanici_id = ?
            ORDER BY islem.tarih DESC
            """,
            (kullanici_id,),
        ).fetchall()
    finally:
        baglanti.close()


def islem_getir(islem_id):
    """R - Tek bir işlemi id'sine göre getirir. Yoksa None döner."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute("SELECT * FROM islem WHERE id = ?", (islem_id,)).fetchone()
    finally:
        baglanti.close()


def islem_guncelle(islem_id, tutar, aciklama):
    """U - Bir işlemin tutarını ve açıklamasını günceller."""
    baglanti = baglanti_al()
    try:
        baglanti.execute(
            "UPDATE islem SET tutar = ?, aciklama = ? WHERE id = ?",
            (tutar, aciklama, islem_id),
        )
        baglanti.commit()
    except sqlite3.Error:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()


def islem_sil(islem_id):
    """D - Bir işlemi siler."""
    baglanti = baglanti_al()
    try:
        baglanti.execute("DELETE FROM islem WHERE id = ?", (islem_id,))
        baglanti.commit()
    except sqlite3.Error:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()


# ---------- Deneme: dosya doğrudan çalıştırılınca CRUD'u ve kısıtları gösterir ----------
if __name__ == "__main__":
    print("--- CRUD DENEMESI ---")
    yeni_id = islem_ekle(2, 4, 120, "2026-11-05", "Taksi")
    print("1) EKLENDI, id:", yeni_id)

    print("2) LISTE:")
    for s in islemleri_listele(2):
        print(f"   #{s['id']}  {s['tarih']}  {s['kategori']:<8} {s['tutar']:>8} TL  {s['aciklama']}")

    islem_guncelle(yeni_id, 150, "Taksi (gece tarifesi)")
    print("3) GUNCELLENDI:", dict(islem_getir(yeni_id)))

    islem_sil(yeni_id)
    print("4) SILINDI, kayit hala var mi?:", islem_getir(yeni_id))

    print("--- KISIT DENEMELERI ---")
    try:
        islem_ekle(2, 3, -50, "2026-11-05", "Eksi tutar")
    except sqlite3.IntegrityError as hata:
        print("Eksi tutar engellendi ->", hata)

    try:
        islem_ekle(99, 3, 50, "2026-11-05", "Olmayan kullanici")
    except sqlite3.IntegrityError as hata:
        print("Olmayan kullanici engellendi ->", hata)