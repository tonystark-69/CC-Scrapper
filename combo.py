import os
#from telegram import Update
from pyrogram import Client
import requests

async def handle_combo(bot: Client, message):
    # Check if the command is replying to a file
    if message.reply_to_message and message.reply_to_message.document:
        file_id = message.reply_to_message.document.file_id

        # Fetch the file from Telegram servers
        file = await bot.get_file(file_id)
        file_content = requests.get(file.file_path).text

        # Process the file content
        lines = file_content.splitlines()
        lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines
        unique_lines = set(lines)
        duplicate_count = len(lines) - len(unique_lines)

        # Check if all lines contain "email:password" format
        valid_format = all(":" in line for line in unique_lines)

        if valid_format:
            # Send the result to the user
            message_text = (
                f"Email:Password found ✅\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"Total: {len(lines)}\n"
                f"Duplicates: {duplicate_count}\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"Combo Cleaner By: Aftab👑"
            )
            await message.reply_text(message_text)
        else:
            await message.reply_text("The file doesn't contain valid email:password combos.")
    else:
        await message.reply_text("Please reply to a valid text file with email:password combos.")
