# Tasarım Belgeleri

## 1. ER Diyagramı

```mermaid
erDiagram
    KULLANICI ||--o{ ISLEM : "yapar"
    KATEGORI ||--o{ ISLEM : "siniflandirir"
    KULLANICI ||--o{ BUTCE_HEDEFI : "belirler"
    KATEGORI ||--o{ BUTCE_HEDEFI : "icin"

    KULLANICI {
        int id PK
        string ad
        string eposta UK
        string parola_hash
        string rol
    }
    KATEGORI {
        int id PK
        string ad UK
        string tur
    }
    ISLEM {
        int id PK
        int kullanici_id FK
        int kategori_id FK
        float tutar
        date tarih
        string aciklama
    }
    BUTCE_HEDEFI {
        int id PK
        int kullanici_id FK
        int kategori_id FK
        float limit_tutar
        string ay
    }
```

### İlişkiler
- **Kullanıcı – İşlem (1-N):** Bir kullanıcının çok işlemi olur, her işlem tek kullanıcıya aittir.
- **Kategori – İşlem (1-N):** Bir kategoride çok işlem olur, her işlemin tek kategorisi vardır.
- **Kullanıcı – Bütçe Hedefi (1-N):** Bir kullanıcı birden çok hedef koyabilir.
- **Kategori – Bütçe Hedefi (1-N):** Bir kategori için farklı aylarda/kullanıcılarda hedef olabilir.
- **Kullanıcı – Kategori (N-N):** Bütçe Hedefi tablosu üzerinden kurulur.

## 2. Mimari Şema (Katmanlı Mimari)

```mermaid
flowchart TD
  A["Kullanıcı - Tarayıcı"] --> B["Sunum Katmanı - sunum/"]
  B --> C["İş Katmanı - is_katmani/"]
  C --> D["Veri Katmanı - veri/"]
  D --> E[("SQLite Veritabanı")]
```