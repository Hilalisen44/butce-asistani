"""
İş katmanı: Gelir/gider işlemleri için kurallar ve doğrulama.
"""
from datetime import date, datetime
from veri import islem_veri, kategori_veri

MAKS_TUTAR = 10_000_000


class IslemHatasi(Exception):
    """Kullanıcıya gösterilecek işlem hatası."""


def islem_kaydet(kullanici_id, kategori_id, tutar, tarih, aciklama):
    """Tüm kuralları kontrol eder, geçerliyse işlemi kaydeder."""
    # Kural 1: Kategori seçilmeli ve gerçekten var olmalı
    try:
        kategori_id = int(kategori_id)
    except (TypeError, ValueError):
        raise IslemHatasi("Lutfen bir kategori secin.")
    if kategori_veri.kategori_getir(kategori_id) is None:
        raise IslemHatasi("Gecersiz kategori.")

    # Kural 2: Tutar sayı olmalı, 0'dan büyük ve makul olmalı
    try:
        tutar = float(str(tutar).replace(",", "."))
    except ValueError:
        raise IslemHatasi("Tutar bir sayi olmali.")
    if tutar <= 0:
        raise IslemHatasi("Tutar 0'dan buyuk olmali.")
    if tutar > MAKS_TUTAR:
        raise IslemHatasi("Tutar cok buyuk.")
    tutar = round(tutar, 2)

    # Kural 3: Tarih geçerli olmalı ve gelecekte olmamalı
    try:
        tarih_obj = datetime.strptime(tarih, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise IslemHatasi("Gecerli bir tarih girin.")
    if tarih_obj > date.today():
        raise IslemHatasi("Gelecek tarihli islem girilemez.")

    # Kural 4: Açıklama en fazla 200 karakter
    aciklama = (aciklama or "").strip()
    if len(aciklama) > 200:
        raise IslemHatasi("Aciklama en fazla 200 karakter olabilir.")

    return islem_veri.islem_ekle(kullanici_id, kategori_id, tutar, tarih_obj.isoformat(), aciklama)


def islem_kaldir(kullanici_id, islem_id):
    """Sadece kendi işlemini silebilir."""
    if islem_veri.islem_sil(islem_id, kullanici_id) == 0:
        raise IslemHatasi("Islem bulunamadi ya da size ait degil.")


def bakiye_ozeti(kullanici_id):
    """Bakiye SAKLANMAZ, her seferinde işlemlerden hesaplanır."""
    toplamlar = islem_veri.tur_toplamlari(kullanici_id)
    gelir = toplamlar.get("gelir", 0) or 0
    gider = toplamlar.get("gider", 0) or 0
    return {"gelir": gelir, "gider": gider, "bakiye": gelir - gider}