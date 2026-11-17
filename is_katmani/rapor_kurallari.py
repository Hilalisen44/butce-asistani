"""
İş katmanı: Panel özeti ve yönetici işlemleri.
"""
import sqlite3
from veri import rapor_veri, islem_veri
from is_katmani.islem_kurallari import bakiye_ozeti
from is_katmani.butce_kurallari import hedef_durumlari, bu_ay


class YonetimHatasi(Exception):
    """Yönetici işlemlerinde kullanıcıya gösterilecek hata."""


def panel_ozeti(kullanici_id):
    """Kullanıcının panelinde gösterilecek her şeyi tek yerde toplar."""
    ay = bu_ay()
    harcamalar = rapor_veri.kategori_harcamalari(kullanici_id, ay)
    en_buyuk = max([h["toplam"] for h in harcamalar], default=0)
    hedefler = hedef_durumlari(kullanici_id, ay)
    return {
        "ay": ay,
        "ozet": bakiye_ozeti(kullanici_id),
        # Her kategorinin çubuk uzunluğu: en çok harcanan kategoriye göre yüzde
        "harcamalar": [
            {"kategori": h["kategori"], "toplam": h["toplam"],
             "yuzde": round(h["toplam"] / en_buyuk * 100) if en_buyuk else 0}
            for h in harcamalar
        ],
        "asilan": [d for d in hedefler if d["durum"] == "asildi"],
        "yaklasan": [d for d in hedefler if d["durum"] == "yaklasiyor"],
        "son_islemler": islem_veri.islemleri_listele(kullanici_id)[:5],
    }


def yonetici_ozeti():
    """Yönetici ekranı için sistem geneli bilgiler."""
    return {
        "sayilar": rapor_veri.genel_sayilar(),
        "kullanicilar": rapor_veri.kullanici_istatistikleri(),
        "kategoriler": rapor_veri.kategori_kullanimi(),
    }


def kategori_olustur(ad, tur):
    """Kuralları kontrol edip yeni kategori ekler."""
    ad = (ad or "").strip()
    if not ad:
        raise YonetimHatasi("Kategori adi bos olamaz.")
    if len(ad) > 30:
        raise YonetimHatasi("Kategori adi en fazla 30 karakter olabilir.")
    if tur not in ("gelir", "gider"):
        raise YonetimHatasi("Tur gelir ya da gider olmali.")
    try:
        rapor_veri.kategori_ekle(ad, tur)
    except sqlite3.IntegrityError:
        raise YonetimHatasi("Bu isimde bir kategori zaten var.")
