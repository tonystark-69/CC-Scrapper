import re
from urllib.parse import urlparse

async def scrape_url_messages(client, channel_username, limit):
    messages = []
    count = 0
    pattern = r'([a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\/[^\s]*)?)'
    async for message in client.search_messages(channel_username):
        if count >= limit:
            break
        text = message.text if message.text else message.caption
        if text:
            matched_urls = re.findall(pattern, text)
            formatted_urls = [urlparse(url).geturl() for url in matched_urls]
            messages.extend(formatted_urls)
            count += len(formatted_urls)
    return messages
