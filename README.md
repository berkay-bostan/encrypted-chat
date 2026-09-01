# Encrypted Chat

Python socket programlama ve Fernet (AES tabanlı) şifreleme kullanan,
PyQt6 arayüzlü, çift yönlü şifreli mesajlaşma uygulaması.

## Özellikler

- Uygulama açılışında Server / Client modu seçimi
- TCP socket üzerinden gerçek zamanlı, çift yönlü mesajlaşma
- Her mesaj Fernet (simetrik AES şifreleme) ile şifrelenip gönderilir
- Threading ile GUI donmadan arka planda mesaj dinleme
- PyQt sinyal/slot mekanizması ile thread-safe arayüz güncellemesi

## Kullanılan Teknolojiler

- Python 3.14
- PyQt6 (arayüz)
- `socket` (TCP bağlantısı)
- `cryptography` / Fernet (şifreleme)
- `threading` (çift yönlü, engellemeyen mesajlaşma)

## Nasıl Çalışır

1. Program açılınca bir mod seçim ekranı gelir: **Server** veya **Client**
2. Server tarafı bir portu dinlemeye başlar (varsayılan: `127.0.0.1:9000`)
3. Client tarafı o adrese bağlanır
4. Bağlantı kurulunca iki taraf da birbirine şifreli mesaj gönderip alabilir
5. Gönderilen her mesaj, ağa çıkmadan önce Fernet ile şifrelenir; alan taraf
   aynı anahtarla deşifre edip ekrana yazar

## Kurulum ve Çalıştırma

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install cryptography PyQt6
python3 gui.py
```

İki ayrı terminalde (veya iki farklı bilgisayarda) çalıştırıp birinde
"Server", diğerinde "Client" seçerek test edebilirsiniz.

## ⚠️ Anahtar Paylaşımı Hakkında

Bu projede kullanılan Fernet şifreleme anahtarı şu an `gui.py` içine
sabit (hardcoded) olarak yazılmıştır. Bu, öğrenme amaçlı bir proje için
kabul edilebilir, ama gerçek bir üründe **asla** yapılmaması gereken bir
şeydir — anahtar kaynak koduyla birlikte paylaşılmamalı, güvenli bir
kanaldan (örn. ayrı bir dosya, ortam değişkeni) sağlanmalıdır.

İki taraf da mesajlaşabilmek için **aynı anahtarı** kullanmak zorundadır.

## Proje Yapısı

encrypted-chat/
├── gui.py              # Mod seçimi + chat arayüzü + network + şifreleme
├── server.py            # (Erken aşama) terminal tabanlı server denemesi
├── client.py             # (Erken aşama) terminal tabanlı client denemesi
├── requirements.txt
└── README.md
