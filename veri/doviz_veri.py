"""
Veri katmanı: Döviz kuru tablosu işlemleri.
"""
import sqlite3
from veri.veritabani import baglanti_al


def kurlari_kaydet(kurlar, zaman):
    """{'USD': 50.42, 'EUR': 58.1, ...} sözlüğünü kaydeder. Varsa günceller (UPSERT)."""
    baglanti = baglanti_al()
    try:
        baglanti.executemany(
            """
            INSERT INTO doviz_kuru (para_birimi, kur, guncellenme) VALUES (?, ?, ?)
            ON CONFLICT(para_birimi) DO UPDATE
            SET kur = excluded.kur, guncellenme = excluded.guncellenme
            """,
            [(birim, kur, zaman) for birim, kur in kurlar.items()],
        )
        baglanti.commit()
    except sqlite3.Error:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()


def kurlari_getir():
    """Kayıtlı kurları getirir: ({'USD': 50.42, ...}, '2026-11-17 16:45') ya da ({}, None)."""
    baglanti = baglanti_al()
    try:
        satirlar = baglanti.execute("SELECT * FROM doviz_kuru").fetchall()
    finally:
        baglanti.close()
    if not satirlar:
        return {}, None
    kurlar = {s["para_birimi"]: s["kur"] for s in satirlar}
    return kurlar, satirlar[0]["guncellenme"]