# 🔗 Flask URL Kısaltıcı (Simple-Shortener) | Kapsamlı Geliştirici Dokümantasyonu

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?style=for-the-badge&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red?style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap%204-purple?style=for-the-badge&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 📑 İçindekiler

1. [Proje Vizyonu ve Mimari](#-proje-vizyonu-ve-mimari)
2. [Teknoloji Yığını ve Seçim Nedenleri](#-teknoloji-yığını-ve-seçim-nedenleri)
3. [Teknik Derinlemesine İnceleme](#-teknik-derinlemesine-inceleme)
    * [Veritabanı Şeması (Schema)](#a-veritabanı-şeması-schema)
    * [Kısaltma Algoritması](#b-kısaltma-algoritması-ve-çarpışma-kontrolü)
    * [HTTP Yönlendirme Mantığı](#c-http-yönlendirme-mantığı)
4. [Kurulum ve Yerel Geliştirme](#-kurulum-ve-yerel-geliştirme)
5. [Kullanım Senaryoları](#-kullanım-senaryoları)
6. [Gelecek Yol Haritası (Roadmap)](#-gelecek-yol-haritası-roadmap)
7. [Sorun Giderme (Troubleshooting)](#-sorun-giderme-troubleshooting)
8. [İletişim ve Lisans](#-iletişim-ve-lisans)

---

## 🎯 Proje Vizyonu ve Mimari

Bu proje, modern web geliştirme prensiplerini uygulayan, **Monolitik** yapıda tasarlanmış bir **URL Kısaltma Servisi (URL Shortener Service)** prototipidir.

Projenin temel amacı; kullanıcı deneyimini ön planda tutarak, uzun ve karmaşık URL'leri veritabanı destekli bir sistem aracılığıyla yönetilebilir, paylaşılabilir ve kısa kodlara (token) dönüştürmektir. Mimari açıdan **MVC (Model-View-Controller)** desenine sadık kalınmıştır:

* **Model:** SQLAlchemy ORM (`UrlKayit` sınıfı).
* **View:** Jinja2 Şablonları ve Bootstrap CSS (`index.html`).
* **Controller:** Flask Rotaları ve İş Mantığı (`app.py`).

---

## 🛠️ Teknoloji Yığını ve Seçim Nedenleri

Projede kullanılan teknolojiler, **performans**, **geliştirme hızı** ve **ölçeklenebilirlik** dengesi gözetilerek seçilmiştir.

| Teknoloji | Tür | Kullanım Nedeni |
| :--- | :--- | :--- |
| **Python 3** | Dil | Okunabilirlik, geniş kütüphane desteği ve hızlı prototipleme yeteneği. |
| **Flask** | Framework | Mikro-framework yapısı sayesinde gereksiz yüklerden arınmış, esnek routing mekanizması. |
| **SQLAlchemy** | ORM | SQL sorgularını Python nesnelerine soyutlayarak veritabanı bağımsızlığı (SQLite/PostgreSQL/MSSQL) sağlar. |
| **SQLite3** | Veritabanı | Sunucu kurulumu gerektirmeyen, dosya tabanlı ve ACID uyumlu yapısı ile geliştirme ortamı için idealdir. |
| **Jinja2** | Template Engine | Python verilerini HTML içine güvenli bir şekilde (XSS koruması ile) enjekte etmek için. |
| **Bootstrap 4** | CSS Framework | Responsive (mobil uyumlu) ve modern UI bileşenleri için. |

---

## 🔬 Teknik Derinlemesine İnceleme

### A. Veritabanı Şeması (Schema)

Veri tutarlılığını sağlamak amacıyla ilişkisel bir veritabanı modeli tasarlanmıştır. Tablo adı: `url_kayit`

```python
class UrlKayit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
