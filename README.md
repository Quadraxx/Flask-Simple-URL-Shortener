# 🔗 Flask URL Kısaltıcı (Simple-Shortener)

## 📝 Proje Hakkında

Bu proje, Python **Flask** mikro web çatısı (framework) ve **SQLite** (yerel veritabanı) kullanılarak geliştirilmiş basit bir URL kısaltma hizmetidir (URL Shortener). Kullanıcıların uzun bağlantıları, benzersiz ve kısa kodlara dönüştürmesini ve bu kodlar aracılığıyla orijinal adrese hızlıca yönlendirilmesini sağlar.

Proje, temel veritabanı işlemleri (CRUD) ve dinamik rota yönetimini öğrenmek amacıyla tasarlanmıştır.

## ✨ Özellikler

* **URL Kısaltma:** Rastgele oluşturulmuş 6 karakterli alfanümerik kısa kodlar üretir.
* **Yönlendirme:** Kısa kodlar kullanılarak orijinal URL'ye anında yönlendirme (redirection).
* **Veritabanı Desteği:** Verilerin yerel olarak depolanması için **SQLite3** kullanır.
* **Arayüz:** Basit Bootstrap temelli kullanıcı arayüzü ile form ve kayıtlı link listesi sunar.

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları takip edin.

### Ön Gereksinimler

* Python 3.x
* `pip` (Python paket yöneticisi)

### 1. Depoyu Klonlama ve Klasöre Geçiş

```bash
git clone [https://github.com/Quadraxx/Flask-Simple-URL-Shortener.git](https://github.com/Quadraxx/Flask-Simple-URL-Shortener.git)
cd Flask-Simple-URL-Shortener
