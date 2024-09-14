from pyrogram import Client

async def scrape_mail_messages(user: Client, chat_id: int, limit: int):
    messages = []
    async for message in user.search_messages(chat_id, limit=limit):
        if message.text:
            # Scrape only the email:password format, excluding other info
            lines = message.text.split("\n")
            for line in lines:
                # Check if the line contains email:password format
                if ":" in line and "@" in line:
                    combo = line.split(" | ")[0].strip()  # Extract the email:password part
                    if combo:
                        messages.append(combo)
    return messages
