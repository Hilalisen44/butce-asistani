"""
Sunum katmanı: Yetki kontrolleri (decorator).
Kontrol SUNUCU tarafında yapılır. Menüden linki gizlemek tek başına yetmez.
"""
from functools import wraps
from flask import session, redirect, url_for, flash, abort


def giris_gerekli(fonksiyon):
    """Giriş yapmamış kullanıcıyı giriş sayfasına gönderir."""
    @wraps(fonksiyon)
    def sarmalayici(*args, **kwargs):
        if not session.get("kullanici_id"):
            flash("Bu sayfayi gormek icin giris yapmalisin.", "hata")
            return redirect(url_for("giris"))
        return fonksiyon(*args, **kwargs)
    return sarmalayici


def yonetici_gerekli(fonksiyon):
    """Sadece 'yonetici' rolündeki kullanıcıların girmesine izin verir."""
    @wraps(fonksiyon)
    def sarmalayici(*args, **kwargs):
        if not session.get("kullanici_id"):
            flash("Bu sayfayi gormek icin giris yapmalisin.", "hata")
            return redirect(url_for("giris"))
        if session.get("rol") != "yonetici":
            abort(403)   # 403 = Yasak (giriş yapmış ama yetkisi yok)
        return fonksiyon(*args, **kwargs)
    return sarmalayici