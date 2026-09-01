# Encrypted Chat

Python socket programlama, Diffie-Hellman anahtar değişimi ve Fernet
(AES tabanlı) şifreleme kullanan, PyQt6 arayüzlü, çift yönlü şifreli
mesajlaşma uygulaması.

## Özellikler

- Uygulama açılışında Server / Client modu seçimi
- TCP socket üzerinden gerçek zamanlı, çift yönlü mesajlaşma
- Bağlantı kurulduğunda Diffie-Hellman ile taraflar arasında **dinamik,
  paylaşılmayan** bir şifreleme anahtarı üretilir
- Her mesaj bu anahtarla Fernet (simetrik AES şifreleme) kullanılarak
  şifrelenip gönderilir
- Threading ile GUI donmadan arka planda mesaj dinleme
- PyQt sinyal/slot mekanizması ile thread-safe arayüz güncellemesi

## Kullanılan Teknolojiler

- Python 3.14
- PyQt6 (arayüz)
- `socket` (TCP bağlantısı)
- `cryptography` / Fernet (mesaj şifreleme)
- Diffie-Hellman anahtar değişimi (RFC 3526, 3072-bit grup) + SHA-256
  (anahtar türetme)
- `threading` (çift yönlü, engellemeyen mesajlaşma)

## Nasıl Çalışır

1. Program açılınca bir mod seçim ekranı gelir: **Server** veya **Client**
2. Server tarafı bir portu dinlemeye başlar (varsayılan: `127.0.0.1:9000`)
3. Client tarafı o adrese bağlanır
4. Bağlantı kurulur kurulmaz, iki taraf **Diffie-Hellman anahtar
   değişimi** yapar: her taraf kendi gizli sayısını üretir, açık
   değerlerini karşılıklı gönderir, ve ağdan hiç geçmeyen ortak bir
   sayıya ulaşır. Bu ortak sayı SHA-256 ile hash'lenip Fernet anahtarına
   çevrilir.
5. Bu andan itibaren gönderilen her mesaj, bu oturuma özel anahtarla
   şifrelenip gönderilir; alan taraf aynı anahtarla deşifre edip
   ekrana yazar

## Kurulum ve Çalıştırma

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install cryptography PyQt6
python3 gui.py
```

İki ayrı terminalde (veya iki farklı bilgisayarda) çalıştırıp birinde
"Server", diğerinde "Client" seçerek test edebilirsiniz.

## ⚠️ Bilinen Sınırlama: Kimlik Doğrulama Yok

Bu projedeki Diffie-Hellman değişimi **kimlik doğrulaması (authentication)
içermez**. Yani teorik olarak biri araya girip (man-in-the-middle) hem
server hem client ile ayrı ayrı anahtar değişimi yapabilir, iki taraf da
karşısındakinin gerçek kişi olduğunu doğrulayamaz. Gerçek dünya
uygulamaları (TLS/HTTPS, Signal gibi) bu açığı sertifikalar veya önceden
doğrulanmış kimlikler ile kapatır. Bu proje, öğrenme amaçlı olduğu için
bu katmanı içermemektedir.

## Proje Yapısı

encrypted-chat/
├── gui.py              # Mod seçimi + chat arayüzü + network + DH anahtar değişimi + şifreleme
├── server.py            # (Erken aşama) terminal tabanlı server denemesi
├── client.py             # (Erken aşama) terminal tabanlı client denemesi
├── dh_test.py            # Diffie-Hellman kavramının izole test dosyası
├── requirements.txt
└── README.md
