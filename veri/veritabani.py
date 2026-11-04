"""
Veri katmanı: Veritabanı bağlantısı ve kurulum.
"""
import sqlite3
from pathlib import Path

# Dosya yolları
KLASOR = Path(__file__).parent              # veri/ klasörü
VERITABANI_YOLU = KLASOR.parent / "butce.db"  # proje ana klasöründe butce.db
SEMA_YOLU = KLASOR / "schema.sql"


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