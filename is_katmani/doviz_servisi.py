"""
İş katmanı: Döviz kuru servisi (harici API entegrasyonu).
- Kurlar 6 saat saklanır (rate limit'e takılmamak için).
- API cevap vermezse uygulama çökmez, son bilinen kur gösterilir.
"""
import os
from datetime import datetime, timedelta

import requests
from veri import doviz_veri

API_URL = os.environ.get("DOVIZ_API_URL", "https://open.er-api.com/v6/latest/USD")
BIRIMLER = ("USD", "EUR", "GBP")
ZAMAN_ASIMI = 5                      # saniye: API 5 sn'de cevap vermezse vazgeç
GECERLILIK = timedelta(hours=6)      # kayıtlı kur 6 saat boyunca kullanılır


class DovizHatasi(Exception):
    """Kur servisiyle ilgili hata."""


def _apiden_cek():
    """API'ye bağlanır, 1 birimin kaç TL olduğunu hesaplar."""
    try:
        cevap = requests.get(API_URL, timeout=ZAMAN_ASIMI)
        cevap.raise_for_status()              # 404, 500 gibi hata kodlarını yakala
        veri = cevap.json()
    except requests.Timeout:
        raise DovizHatasi("Kur servisi zamaninda cevap vermedi.")
    except (requests.RequestException, ValueError):
        raise DovizHatasi("Kur servisine ulasilamadi.")

    # Gelen cevap beklediğimiz gibi mi? (doğrulama)
    oranlar = veri.get("rates", {})
    if veri.get("result") != "success" or "TRY" not in oranlar:
        raise DovizHatasi("Kur servisinden gecersiz cevap geldi.")

    try:
        # API dolar bazlı: 1 USD = 50.42 TRY, 1 USD = 0.86 EUR → 1 EUR = 50.42 / 0.86 TL
        return {b: round(oranlar["TRY"] / oranlar[b], 4) for b in BIRIMLER}
    except (KeyError, ZeroDivisionError, TypeError):
        raise DovizHatasi("Kur servisinden eksik veri geldi.")


def guncel_kurlar():
    """Kurları döndürür: önce kayıtlıya bakar, eskiyse API'den yeniler, API bozuksa eskiyi kullanır."""
    kayitli, zaman = doviz_veri.kurlari_getir()

    # 1) Kayıtlı kur taze mi? (6 saatten yeni) → API'ye hiç gitme
    if kayitli and datetime.now() - datetime.fromisoformat(zaman) < GECERLILIK:
        return {"kurlar": kayitli, "guncellenme": zaman, "uyari": None}

    # 2) Değilse API'den yeni kur çek ve kaydet
    try:
        yeni = _apiden_cek()
        simdi = datetime.now().strftime("%Y-%m-%d %H:%M")
        doviz_veri.kurlari_kaydet(yeni, simdi)
        return {"kurlar": yeni, "guncellenme": simdi, "uyari": None}

    # 3) API bozuksa: elimizde eski kur varsa onu göster, yoksa uyar
    except DovizHatasi as hata:
        if kayitli:
            return {"kurlar": kayitli, "guncellenme": zaman,
                    "uyari": f"{hata} Son bilinen kurlar gosteriliyor."}
        return {"kurlar": {}, "guncellenme": None,
                "uyari": f"{hata} Kur bilgisi su an gosterilemiyor."}


def tl_cevir(tutar_tl, kurlar):
    """TL tutarı dövizlere çevirir: 11550 TL → {'USD': 229.08, 'EUR': ...}"""
    return {b: tutar_tl / k for b, k in kurlar.items()}