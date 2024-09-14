import re

async def scrape_mail_messages(client, channel_username, limit, start_number=None):
    messages = []
    count = 0
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+:[^\s|]+'  # Updated to handle more complex cases

    async for message in client.search_messages(channel_username):
        if count >= limit:
            break
        text = message.text if message.text else message.caption
        if text:
            matched_messages = re.findall(pattern, text)
            if matched_messages:
                formatted_messages = []
                for matched_message in matched_messages:
                    formatted_messages.append(matched_message)
                messages.extend(formatted_messages)
                count += len(formatted_messages)
    if start_number:
        messages = [msg for msg in messages if msg.startswith(start_number)]
    return messages
