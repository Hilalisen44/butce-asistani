-- Bütçe Asistanı veritabanı şeması (DDL)

CREATE TABLE IF NOT EXISTS kullanici (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    ad           TEXT NOT NULL,
    eposta       TEXT NOT NULL UNIQUE,
    parola_hash  TEXT NOT NULL,
    rol          TEXT NOT NULL DEFAULT 'kullanici'
                 CHECK (rol IN ('kullanici', 'yonetici'))
);

CREATE TABLE IF NOT EXISTS kategori (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    ad   TEXT NOT NULL UNIQUE,
    tur  TEXT NOT NULL CHECK (tur IN ('gelir', 'gider'))
);

CREATE TABLE IF NOT EXISTS islem (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_id  INTEGER NOT NULL,
    kategori_id   INTEGER NOT NULL,
    tutar         REAL NOT NULL CHECK (tutar > 0),
    tarih         TEXT NOT NULL,
    aciklama      TEXT,
    FOREIGN KEY (kullanici_id) REFERENCES kullanici(id) ON DELETE CASCADE,
    FOREIGN KEY (kategori_id)  REFERENCES kategori(id)  ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS butce_hedefi (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_id  INTEGER NOT NULL,
    kategori_id   INTEGER NOT NULL,
    limit_tutar   REAL NOT NULL CHECK (limit_tutar > 0),
    ay            TEXT NOT NULL,
    FOREIGN KEY (kullanici_id) REFERENCES kullanici(id) ON DELETE CASCADE,
    FOREIGN KEY (kategori_id)  REFERENCES kategori(id)  ON DELETE RESTRICT,
    UNIQUE (kullanici_id, kategori_id, ay)
);

-- İndeksler: sık aranan sütunlarda aramayı hızlandırır
CREATE INDEX IF NOT EXISTS idx_islem_kullanici_tarih ON islem(kullanici_id, tarih);
CREATE INDEX IF NOT EXISTS idx_islem_kategori ON islem(kategori_id);