import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, SESSION_STRING, BOT_TOKEN, ADMIN_IDS, DEFAULT_LIMIT, ADMIN_LIMIT
from scr import scrape_cc_messages
from scrurl import scrape_url_messages
from scrmail import scrape_mail_messages
from combo import handle_combo
from keep_alive import keep_alive

# Initialize the bot and user clients
bot = Client(
    "bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    parse_mode=ParseMode.HTML
)

user = Client(
    "user_session",
    session_string=SESSION_STRING,
    workers=1000
)

def remove_duplicates(messages):
    unique_messages = list(set(messages))
    duplicates_removed = len(messages) - len(unique_messages)
    return unique_messages, duplicates_removed

# /start command
@bot.on_message(filters.command(["start"]))
async def start_cmd(client, message):
    welcome_text = (
        "<b>Welcome to the Scraper Bot!</b>\n\n"
        "You can use the following commands:\n"
        "1. <code>/scr &lt;channel&gt; &lt;limit&gt;</code> - Scrape credit card data.\n"
        "2. <code>/scrurl &lt;channel&gt; &lt;limit&gt;</code> - Scrape URLs.\n"
        "3. <code>/scrmail &lt;channel&gt; &lt;limit&gt;</code> - Scrape email:password combos.\n"
        "4. <code>/combo</code> - Check email:password combos in a text file.\n"
        "Example: <code>/scr @channel 100</code>\n\n"
        "For any issues, contact the bot creator: <a href='https://t.me/aftab_kabirr'>Aftab👑</a>"
    )
    await message.reply_text(welcome_text)

# /scr command to scrape credit card data
@bot.on_message(filters.command(["scr"]))
async def scr_cmd(client, message):
    args = message.text.split()[1:]
    if len(args) < 2 or len(args) > 3:
        await message.reply_text("<b>⚠️ Provide channel username and amount to scrape</b>")
        return
    channel_identifier = args[0]
    limit = int(args[1])
    max_lim = ADMIN_LIMIT if message.from_user.id in ADMIN_IDS else DEFAULT_LIMIT
    if limit > max_lim:
        await message.reply_text(f"<b>Sorry Bro! Amount over Max limit is {max_lim} ❌</b>")
        return
    start_number = args[2] if len(args) == 3 else None

    try:
        chat = await user.get_chat(channel_identifier)
        channel_name = chat.title
    except Exception:
        await message.reply_text("<b>Hey Bro! 🥲 Incorrect username ❌</b>")
        return

    temporary_msg = await message.reply_text("<b>Scraping in progress wait.....</b>")
    scrapped_results = await scrape_cc_messages(user, chat.id, limit, start_number)
    unique_messages, duplicates_removed = remove_duplicates(scrapped_results)
    
    if unique_messages:
        file_name = f"x{len(unique_messages)}_{channel_name.replace(' ', '_')}.txt"
        with open(file_name, 'w') as f:
            f.write("\n".join(unique_messages))
        with open(file_name, 'rb') as f:
            caption = (
                f"<b>CC Scrapped Successfully ✅</b>\n"
                f"<b>━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Source:</b> <code>{channel_name}</code>\n"
                f"<b>Amount:</b> <code>{len(unique_messages)}</code>\n"
                f"<b>Duplicates Removed:</b> <code>{duplicates_removed}</code>\n"
                f"<b>━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Card-Scraper By: <a href='https://t.me/aftab_kabirr'>Aftab👑</a></b>\n"
            )
            await temporary_msg.delete()
            await client.send_document(message.chat.id, f, caption=caption)
        os.remove(file_name)
    else:
        await temporary_msg.delete()
        await client.send_message(message.chat.id, "<b>Sorry Bro ❌ No Credit Card Found</b>")

# /scrurl command to scrape URLs
@bot.on_message(filters.command(["scrurl"]))
async def scrurl_cmd(client, message):
    args = message.text.split()[1:]
    if len(args) < 2:
        await message.reply_text("<b>⚠️ Provide channel username and amount to scrape</b>")
        return
    channel_identifier = args[0]
    limit = int(args[1])

    try:
        chat = await user.get_chat(channel_identifier)
        channel_name = chat.title
    except Exception:
        await message.reply_text("<b>Hey Bro! 🥲 Incorrect username ❌</b>")
        return

    temporary_msg = await message.reply_text("<b>Scraping URLs in progress, wait.....</b>")
    scrapped_results = await scrape_url_messages(user, chat.id, limit)
    unique_messages, duplicates_removed = remove_duplicates(scrapped_results)
    
    if unique_messages:
        file_name = f"x{len(unique_messages)}_{channel_name.replace(' ', '_')}_urls.txt"
        with open(file_name, 'w') as f:
            f.write("\n".join(unique_messages))
        with open(file_name, 'rb') as f:
            caption = (
                f"<b>URLs Scrapped Successfully ✅</b>\n"
                f"<b>━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Source:</b> <code>{channel_name}</code>\n"
                f"<b>Amount:</b> <code>{len(unique_messages)}</code>\n"
                f"<b>Duplicates Removed:</b> <code>{duplicates_removed}</code>\n"
                f"<b>━━━━━━━━━━━━━━━━</b>\n"
                f"<b>URL-Scraper By: <a href='https://t.me/aftab_kabirr'>Aftab👑</a></b>\n"
            )
            await temporary_msg.delete()
            await client.send_document(message.chat.id, f, caption=caption)
        os.remove(file_name)
    else:
        await temporary_msg.delete()
        await client.send_message(message.chat.id, "<b>Sorry Bro ❌ No URLs Found</b>")

# /scrmail command to scrape email:password combos
@bot.on_message(filters.command(["scrmail"]))
async def scrmail_cmd(client, message):
    args = message.text.split()[1:]
    if len(args) < 2:
        await message.reply_text("<b>⚠️ Provide channel username and amount to scrape</b>")
        return
    channel_identifier = args[0]
    limit = int(args[1])

    try:
        chat = await user.get_chat(channel_identifier)
        channel_name = chat.title
    except Exception:
        await message.reply_text("<b>Hey Bro! 🥲 Incorrect username ❌</b>")
        return

    temporary_msg = await message.reply_text("<b>Scraping emails in progress, wait.....</b>")
    scrapped_results = await scrape_mail_messages(user, chat.id, limit)
    unique_messages, duplicates_removed = remove_duplicates(scrapped_results)
    
    if unique_messages:
        file_name = f"x{len(unique_messages)}_{channel_name.replace(' ', '_')}_mails.txt"
        with open(file_name, 'w') as f:
            f.write("\n".join(unique_messages))
        with open(file_name, 'rb') as f:
            caption = (
                f"<b>Emails Scrapped Successfully ✅</b>\n"
                f"<b>━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Source:</b> <code>{channel_name}</code>\n"
                f"<b>Amount:</b> <code>{len(unique_messages)}</code>\n"
                f"<b>Duplicates Removed:</b> <code>{duplicates_removed}</code>\n"
                f"<b>━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Email-Scraper By: <a href='https://t.me/aftab_kabirr'>Aftab👑</a></b>\n"
            )
            await temporary_msg.delete()
            await client.send_document(message.chat.id, f, caption=caption)
        os.remove(file_name)
    else:
        await temporary_msg.delete()
        await client.send_message(message.chat.id, "<b>Sorry Bro ❌ No Emails Found</b>")

# /combo command to check combos
@bot.on_message(filters.command(["combo"]) & filters.reply)
async def combo_cmd(client, message):
    await handle_combo(client, message)  # Call the function from combo.py



if __name__ == "__main__":
    keep_alive()  # Start the keep-alive server
    user.start()  # Start the user client
    bot.run()     # Start the bot client
