# web.py

import requests
import redis
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def get_page(url: str) -> str:
    # Check cache first
    cached_html = r.get(url)
    if cached_html:
        # Return cached HTML content
        return cached_html.decode('utf-8')

    # If not cached, fetch from URL
    response = requests.get(url)
    html_content = response.text

    # Cache the HTML with expiration time of 10 seconds
    r.setex(url, 10, html_content)

    # Track access count
    count_key = f"count:{url}"
    r.incr(count_key)

    return html_content
