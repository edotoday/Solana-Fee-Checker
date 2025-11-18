# checker.py
import time
import requests
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, FEE_THRESHOLD_MICROLAMPORTS, CHECK_INTERVAL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Публичный эндпоинт (Helius бесплатный прокси)
API_URL = "https://api.mainnet-beta.solana.com"

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getRecentPrioritizationFees",
    "params": []
}

last_notified_fee = None
notified_low = False

def get_median_priority_fee():
    try:
        r = requests.post(API_URL, json=payload, timeout=10)
        if r.status_code == 200:
            data = r.json()
            fees = [slot["prioritizationFee"] for slot in data["result"]]
            if not fees:
                return None
            median = sorted(fees)[len(fees)//2]
            return median  # в microlamports
        else:
            logging.error(f"RPC error: {r.status_code}")
            return None
    except Exception as e:
        logging.error(f"Request failed: {e}")
        return None

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        logging.error(f"Telegram error: {e}")

def main():
    global last_notified_fee, notified_low

    logging.info("Solana Fee Checker запущен")
    send_telegram_message("Solana Priority Fee Checker запущен\nЖду низкие комиссии...")

    while True:
        fee = get_median_priority_fee()
        if fee is None:
            time.sleep(CHECK_INTERVAL)
            continue

        # Переводим в lamports для удобства (1 microlamport = 0.000001 lamport)
        fee_lamports = fee / 1_000_000

        message = f"<b>Solana Priority Fee</b>\n<code>{fee_lamports:.6f}</code> lamports (~{fee:,} microlamports)"

        should_notify = False

        if fee <= FEE_THRESHOLD_MICROLAMPORTS and not notified_low:
            should_notify = True
            notified_low = True
            message = f"<b>НИЗКАЯ КОМИССИЯ НА SOLANA!</b>\n<code>{fee_lamports:.6f}</code> lamports\nСНАЙПИ СЕЙЧАС! Jupiter / Raydium / Pump.fun"
        elif fee > FEE_THRESHOLD_MICROLAMPORTS and notified_low:
            should_notify = True
            notified_low = False
            message = f"Комиссия выросла: <code>{fee_lamports:.6f}</code> lamports"

        if last_notified_fee is not None and abs(fee - last_notified_fee) >= 5000:  # каждые 5000 microlamports
            should_notify = True

        if should_notify or last_notified_fee is None:
            logging.info(f"Fee: {fee_lamports:.6f} lamports")
            send_telegram_message(message)
            last_notified_fee = fee

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
