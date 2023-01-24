from pyrate_limiter import Duration, RequestRate, Limiter

LOGIN_RATE_LIMIT = Limiter(RequestRate(3, Duration.MINUTE))
CHAT_RATE_LIMIT = Limiter(RequestRate(1, Duration.SECOND))