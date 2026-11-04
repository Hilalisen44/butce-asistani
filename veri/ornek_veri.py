"""
Veri katmanı: Örnek (sentetik) veri ekleme.
KVKK: Gerçek kişisel veri kullanılmaz. Tüm isim ve e-postalar uydurmadır.
"""
from werkzeug.security import generate_password_hash
from veri.veritabani import baglanti_al, veritabanini_kur

KATEGORILER = [
    ("Maaş", "gelir"),     # id 1
    ("Burs", "gelir"),     # id 2
    ("Market", "gider"),   # id 3
    ("Ulaşım", "gider"),   # id 4
    ("Fatura", "gider"),   # id 5
    ("Eğlence", "gider"),  # id 6
]


def ornek_veri_ekle():
    veritabanini_kur()
    baglanti = baglanti_al()

    # 1) Eski verileri temizle (dosya tekrar çalışınca çift kayıt olmasın)
    baglanti.execute("DELETE FROM islem")
    baglanti.execute("DELETE FROM butce_hedefi")
    baglanti.execute("DELETE FROM kullanici")
    baglanti.execute("DELETE FROM kategori")
    baglanti.execute("DELETE FROM sqlite_sequence")  # numaralar 1'den başlasın

    # 2) Kullanıcılar (parola düz metin DEĞİL, hash'lenmiş saklanır)
    baglanti.execute(
        "INSERT INTO kullanici (ad, eposta, parola_hash, rol) VALUES (?, ?, ?, ?)",
        ("Deneme Yonetici", "yonetici@ornek.com", generate_password_hash("Yonetici123"), "yonetici"),
    )
    baglanti.execute(
        "INSERT INTO kullanici (ad, eposta, parola_hash, rol) VALUES (?, ?, ?, ?)",
        ("Test Kullanici", "test@ornek.com", generate_password_hash("Test123"), "kullanici"),
    )

    # 3) Kategoriler
    baglanti.executemany("INSERT INTO kategori (ad, tur) VALUES (?, ?)", KATEGORILER)

    # 4) İşlemler: (kullanici_id, kategori_id, tutar, tarih, aciklama)
    islemler = [
        (2, 1, 15000, "2026-11-01", "Kasim maasi"),
        (2, 3, 850,   "2026-11-02", "Haftalik market"),
        (2, 4, 300,   "2026-11-03", "Otobus karti"),
        (2, 5, 650,   "2026-11-03", "Elektrik faturasi"),
        (2, 6, 400,   "2026-11-04", "Sinema"),
        (2, 3, 1250,  "2026-11-04", "Aylik market"),
    ]
    baglanti.executemany(
        "INSERT INTO islem (kullanici_id, kategori_id, tutar, tarih, aciklama) VALUES (?, ?, ?, ?, ?)",
        islemler,
    )

    # 5) Bütçe hedefleri: (kullanici_id, kategori_id, limit_tutar, ay)
    hedefler = [
        (2, 3, 2000, "2026-11"),  # Market limiti 2000 TL
        (2, 6, 300,  "2026-11"),  # Eğlence limiti 300 TL (bilerek aşıldı: 400 TL harcandı)
    ]
    baglanti.executemany(
        "INSERT INTO butce_hedefi (kullanici_id, kategori_id, limit_tutar, ay) VALUES (?, ?, ?, ?)",
        hedefler,
    )

    baglanti.commit()   # değişiklikleri kalıcı olarak kaydet
    baglanti.close()
    print("Ornek veriler eklendi.")


if __name__ == "__main__":
    ornek_veri_ekle()