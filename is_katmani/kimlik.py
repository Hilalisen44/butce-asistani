"""
İş katmanı: Kayıt ve giriş kuralları.
"""
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from veri import kullanici_veri


class KimlikHatasi(Exception):
    """Kayıt/giriş sırasında kullanıcıya gösterilecek hata."""


def kayit_ol(ad, eposta, parola):
    """Kuralları kontrol eder, parolayı hash'ler ve kullanıcıyı kaydeder."""
    ad = ad.strip()
    eposta = eposta.strip().lower()

    # İş kuralları (doğrulama)
    if not ad or not eposta or not parola:
        raise KimlikHatasi("Tum alanlari doldurun.")
    if "@" not in eposta:
        raise KimlikHatasi("Gecerli bir e-posta girin.")
    if len(parola) < 6:
        raise KimlikHatasi("Parola en az 6 karakter olmali.")

    parola_hash = generate_password_hash(parola)
    try:
        return kullanici_veri.kullanici_ekle(ad, eposta, parola_hash)
    except sqlite3.IntegrityError:
        raise KimlikHatasi("Bu e-posta ile zaten bir hesap var.")


def giris_dogrula(eposta, parola):
    """E-posta ve parola doğruysa kullanıcıyı döndürür, değilse hata verir."""
    kullanici = kullanici_veri.eposta_ile_getir(eposta.strip().lower())
    if kullanici is None or not check_password_hash(kullanici["parola_hash"], parola):
        raise KimlikHatasi("E-posta veya parola hatali.")
    return kullanici