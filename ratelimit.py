from pyrate_limiter import Duration, RequestRate, Limiter

""" Login request rate limit """
LOGIN_RATE_LIMIT = Limiter(RequestRate(3, Duration.SECOND))