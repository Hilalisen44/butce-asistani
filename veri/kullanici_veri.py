"""
Veri katmanı: Kullanıcı tablosu işlemleri.
"""
import sqlite3
from veri.veritabani import baglanti_al


def kullanici_ekle(ad, eposta, parola_hash, rol="kullanici"):
    """Yeni kullanıcı ekler, id'sini döndürür."""
    baglanti = baglanti_al()
    try:
        imlec = baglanti.execute(
            "INSERT INTO kullanici (ad, eposta, parola_hash, rol) VALUES (?, ?, ?, ?)",
            (ad, eposta, parola_hash, rol),
        )
        baglanti.commit()
        return imlec.lastrowid
    except sqlite3.Error:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()


def eposta_ile_getir(eposta):
    """E-postaya göre kullanıcıyı getirir. Yoksa None döner."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute(
            "SELECT * FROM kullanici WHERE eposta = ?", (eposta,)
        ).fetchone()
    finally:
        baglanti.close()


def id_ile_getir(kullanici_id):
    """id'ye göre kullanıcıyı getirir. Yoksa None döner."""
    baglanti = baglanti_al()
    try:
        return baglanti.execute(
            "SELECT * FROM kullanici WHERE id = ?", (kullanici_id,)
        ).fetchone()
    finally:
        baglanti.close()