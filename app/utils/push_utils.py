import asyncio, httpx, time
from cachetools import TTLCache

PUSH_URL     = "https://exp.host/--/api/v2/push/send"
RECEIPT_URL  = "https://exp.host/--/api/v2/push/getReceipts"
CACHE_TTL    = 60 * 10          # 保存 10 分钟即可
CACHE_MAX    = 10_000           # 最多 1 万条映射（~1 MB 内存）
receipt_map  = TTLCache(maxsize=CACHE_MAX, ttl=CACHE_TTL)
cache_lock   = asyncio.Lock()   # 保证并发安全