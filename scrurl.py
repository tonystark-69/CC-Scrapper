import re

async def scrape_url_messages(client, channel_username, limit):
    messages = []
    count = 0

    # This regex will capture both full URLs with http(s) and domain names without a protocol
    url_pattern = r'(https?://[^\s]+|\b[\w-]+\.\w{2,}\b)'

    async for message in client.search_messages(channel_username):
        if count >= limit:
            break
        text = message.text if message.text else message.caption
        if text:
            matched_urls = re.findall(url_pattern, text)
            if matched_urls:
                messages.extend(matched_urls)
                count += len(matched_urls)
    return messages
