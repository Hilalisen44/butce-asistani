"""
İş katmanı: Bütçe hedefi kuralları ve aşım uyarısı.
"""
import re
from datetime import date
from veri import butce_veri, kategori_veri

UYARI_ESIGI = 0.80   # Limitin %80'ine gelince "yaklasiyor" uyarisi


class ButceHatasi(Exception):
    """Kullanıcıya gösterilecek bütçe hatası."""


def bu_ay():
    """Bugünün ayını '2026-11' biçiminde verir."""
    return date.today().strftime("%Y-%m")


def hedef_belirle(kullanici_id, kategori_id, limit_tutar, ay):
    """Kuralları kontrol eder, geçerliyse hedefi kaydeder/günceller."""
    # Kural 1: Kategori var olmalı ve GİDER kategorisi olmalı
    try:
        kategori_id = int(kategori_id)
    except (TypeError, ValueError):
        raise ButceHatasi("Lutfen bir kategori secin.")
    kategori = kategori_veri.kategori_getir(kategori_id)
    if kategori is None:
        raise ButceHatasi("Gecersiz kategori.")
    if kategori["tur"] != "gider":
        raise ButceHatasi("Butce hedefi sadece gider kategorilerine konabilir.")

    # Kural 2: Limit sayı olmalı ve 0'dan büyük olmalı
    try:
        limit_tutar = float(str(limit_tutar).replace(",", "."))
    except ValueError:
        raise ButceHatasi("Limit bir sayi olmali.")
    if limit_tutar <= 0:
        raise ButceHatasi("Limit 0'dan buyuk olmali.")

    # Kural 3: Ay YYYY-AA biçiminde olmalı
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", ay or ""):
        raise ButceHatasi("Ay YYYY-AA biciminde olmali.")

    butce_veri.hedef_kaydet(kullanici_id, kategori_id, round(limit_tutar, 2), ay)


def hedef_durumlari(kullanici_id, ay):
    """Her hedef için harcanan, kalan, yüzde ve durumu (normal/yaklasiyor/asildi) hesaplar."""
    durumlar = []
    for h in butce_veri.hedefleri_listele(kullanici_id, ay):
        oran = h["harcanan"] / h["limit_tutar"]
        if oran > 1:
            durum = "asildi"
        elif oran >= UYARI_ESIGI:
            durum = "yaklasiyor"
        else:
            durum = "normal"
        durumlar.append({
            "id": h["id"],
            "kategori_id": h["kategori_id"],
            "kategori": h["kategori"],
            "limit": h["limit_tutar"],
            "harcanan": h["harcanan"],
            "kalan": h["limit_tutar"] - h["harcanan"],
            "yuzde": round(oran * 100),
            "durum": durum,
        })
    return durumlar


def kategori_uyarisi(kullanici_id, kategori_id, tarih):
    """Yeni harcamadan sonra o kategorinin hedefi aşıldı ya da yaklaştıysa uyarı metni döndürür."""
    ay = tarih[:7]
    for d in hedef_durumlari(kullanici_id, ay):
        if d["kategori_id"] == int(kategori_id):
            if d["durum"] == "asildi":
                return f"DIKKAT! {d['kategori']} butceni astin: {d['harcanan']:.2f} / {d['limit']:.2f} TL"
            if d["durum"] == "yaklasiyor":
                return f"{d['kategori']} butcenin %{d['yuzde']}'ini kullandin."
    return None


def hedef_kaldir(kullanici_id, hedef_id):
    """Sadece kendi hedefini silebilir."""
    if butce_veri.hedef_sil(hedef_id, kullanici_id) == 0:
        raise ButceHatasi("Hedef bulunamadi ya da size ait degil.")