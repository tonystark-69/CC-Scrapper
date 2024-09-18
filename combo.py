import os

async def handle_combo(bot, message):
    # Check if a document (txt file) is attached
    if not message.document or not message.document.file_name.endswith(".txt"):
        await message.reply_text("<b>❌ Please reply with a valid .txt file containing email:password combos</b>")
        return

    file_id = message.document.file_id
    
    # Download the file
    file_path = await bot.download_media(file_id)
    
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()

        # Count total lines and check for duplicates
        total_lines = len(lines)
        unique_lines = list(set(lines))
        duplicates_removed = total_lines - len(unique_lines)

        if total_lines > 0:
            # Reply with the result
            await message.reply_text(
                f"<b>Email:Password found ✅</b>\n"
                f"<b>━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Total:</b> {total_lines}\n"
                f"<b>Duplicates:</b> {duplicates_removed}\n"
                f"<b>━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Combo Cleaner By: Aftab👑</b>"
            )
        else:
            await message.reply_text("<b>❌ The file is empty!</b>")
    
    finally:
        # Clean up the downloaded file
        if os.path.exists(file_path):
            os.remove(file_path)
