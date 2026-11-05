"""
Veri katmanı: Veritabanı bağlantısı ve kurulum.
"""
import sqlite3
from pathlib import Path

import sys

# Dosya yolları
KLASOR = Path(__file__).parent              # veri/ klasörü
SEMA_YOLU = KLASOR / "schema.sql"

if getattr(sys, "frozen", False):
    # .exe olarak çalışıyorsa: veritabanı exe'nin yanında dursun
    VERITABANI_YOLU = Path(sys.executable).parent / "butce.db"
else:
    # normal (python app.py) çalışıyorsa: proje ana klasöründe
    VERITABANI_YOLU = KLASOR.parent / "butce.db"

def baglanti_al():
    """Veritabanına bağlanır ve bağlantıyı döndürür."""
    baglanti = sqlite3.connect(VERITABANI_YOLU)
    baglanti.row_factory = sqlite3.Row             # sonuçlara sütun adıyla erişmek için
    baglanti.execute("PRAGMA foreign_keys = ON")   # yabancı anahtar kontrolünü aç
    return baglanti


def veritabanini_kur():
    """schema.sql dosyasını okuyup tabloları oluşturur."""
    sema = SEMA_YOLU.read_text(encoding="utf-8")
    baglanti = baglanti_al()
    baglanti.executescript(sema)
    baglanti.close()
    print("Veritabani hazir:", VERITABANI_YOLU)


if __name__ == "__main__":
    veritabanini_kur()