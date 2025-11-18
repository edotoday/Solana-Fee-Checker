# ⚡ Solana Priority Fee Checker + Telegram Alerts

Самый быстрый чекер приоритетных комиссий **Solana** с мгновенными уведомлениями в Telegram, когда сеть становится дешёвой.

Подходит идеально для снайперов **Jupiter, Raydium, Pump.fun, Tensor** и всех мемкоин-охотников, которым важна скорость и минимальная комиссия.

---

## 🚀 Особенности
- Проверка каждые **6 секунд** через официальный RPC  
- Уведомления только если комиссия **≤ заданного порога**
- Сообщение, когда комиссия снова выросла  
- **Без платных RPC** — использует публичные эндпоинты  
- Работает **24/7** на VPS или домашнем ПК  

---

## 📦 Установка и запуск

### 1. Клонирование проекта

```bash
git clone https://github.com/edotoday/solana-fee-checker.git
cd solana-fee-checker
```

---

### 2. Установка зависимостей

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3. Настройка `.env`

```bash
cp .env.example .env
nano .env
```

Пример (рекомендуемые значения):

```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=-1001234567890
FEE_THRESHOLD_MICROLAMPORTS=3000     # ≤0.003 lamports — отличный момент для снайпа
CHECK_INTERVAL=6
```

---

## 🤖 Создание Telegram-бота

1. Написать **@BotFather**  
2. Команда `/newbot` → придумать имя  
3. Получить токен  
4. Написать боту любое сообщение  
5. Узнать `chat_id`:  

```
https://api.telegram.org/bot<ТОКЕН>/getUpdates
```

---

## ▶️ Запуск

```bash
python checker.py
```

После запуска бот отправит сообщение:

**«Solana Priority Fee Checker запущен»**

---

## 🟢 Запуск 24/7

### 1) Через `screen` (простой способ)

```bash
screen -S solfee
python checker.py
```

Отсоединиться: **Ctrl + A**, затем **D**  
Вернуться:

```bash
screen -r solfee
```

---

### 2) Через `systemd` (идеально для VPS)

Создать сервис:

```bash
sudo nano /etc/systemd/system/solfee.service
```

Вставить:

```ini
[Unit]
Description=Solana Fee Checker
After=network.target

[Service]
WorkingDirectory=/home/user/solana-fee-checker
ExecStart=/home/user/solana-fee-checker/venv/bin/python /home/user/solana-fee-checker/checker.py
Restart=always
RestartSec=10
User=user

[Install]
WantedBy=multi-user.target
```

Активировать:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now solfee.service
```

---

## 🎯 Готово!

Теперь ты никогда не пропустишь момент, когда на Solana можно **снайпить за копейки**.

**Автор:** [@edotoday_eth](https://x.com/edotoday_eth)

Удачных снайпов и жирных **1000x** на Solana! 🫡🔥
