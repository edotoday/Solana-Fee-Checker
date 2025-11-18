from decouple import config

TELEGRAM_BOT_TOKEN         = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID           = config('TELEGRAM_CHAT_ID')
FEE_THRESHOLD_MICROLAMPORTS = config('FEE_THRESHOLD_MICROLAMPORTS', default=3000, cast=int)  # 0.003 lamports
CHECK_INTERVAL             = config('CHECK_INTERVAL', default=6, cast=int)
