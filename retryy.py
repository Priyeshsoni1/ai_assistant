import random
import time

from functools import wraps


MAX_RETRIES = 5
BASE_DELAY = 1


def calculate_delay(attempt: int) -> float:
    """
    Exponential backoff with jitter.

    Attempt 0 -> ~1 sec
    Attempt 1 -> ~2 sec
    Attempt 2 -> ~4 sec
    Attempt 3 -> ~8 sec
    Attempt 4 -> ~16 sec
    """

    exponential_delay = BASE_DELAY * (2 ** attempt)

    jitter = random.uniform(0, 1)

    return exponential_delay + jitter


def is_retryable(error: Exception) -> bool:
    """
    Returns True if the error is worth retrying.
    """

    error_text = str(error).lower()

    retryable_patterns = [
    
        "429",
        "500",
        "502",
        "503",
        "504",
        "timeout",
        "connection",
        "rate limit",
    ]

    return any(
        pattern in error_text
        for pattern in retryable_patterns
    )


def retry_with_backoff(func):
    """
    Decorator for retrying transient API failures.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        for attempt in range(MAX_RETRIES):

            try:
                return func(*args, **kwargs)

            except Exception as error:

                # Don't retry non-transient errors
                if not is_retryable(error):
                    raise

                # Last attempt
                if attempt == MAX_RETRIES - 1:

                    print(
                        f"\nMaximum retries exceeded "
                        f"({MAX_RETRIES})"
                    )

                    raise

                delay = calculate_delay(attempt)

                print(
                    f"\nRetry {attempt + 1}/{MAX_RETRIES}"
                )

                print(
                    f"Reason: {error}"
                )

                print(
                    f"Waiting {delay:.2f}s..."
                )

                time.sleep(delay)

    return wrapper