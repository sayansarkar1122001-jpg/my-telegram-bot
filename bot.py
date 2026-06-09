import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatMemberStatus
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Render se TOKEN uthane ke liye ye system add kiya hai
TOKEN = os.getenv('TOKEN') 
CHANNELS = ["@Muse_India_Dual_Audio", "@MUSE_INDIAN2", "@Naruto_Shippuden_Hindi_Link", "@Wind_Breaker_Hindi_Link"]

async def is_subscribed(context, user_id):
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            # LEFT aur BANNED status matlab user ne join nahi kiya hai
            if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
                return False
        except Exception as e:
            print(f"Error checking {channel}: {e}")
            return False 
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_subscribed(context, user_id):
        await update.message.reply_text("Sahi hai! Aapne saare channels join kar liye hain.")
    else:
        # Sabhi 4 channels ke buttons yahan add kar diye
        keyboard = [
            [InlineKeyboardButton("Join Channel 1", url="https://t.me/Muse_India_Dual_Audio")],
            [InlineKeyboardButton("Join Channel 2", url="https://t.me/MUSE_INDIAN2")],
            [InlineKeyboardButton("Join Channel 3", url="https://t.me/Naruto_Shippuden_Hindi_Link")],
            [InlineKeyboardButton("Join Channel 4", url="https://t.me/Wind_Breaker_Hindi_Link")],
            [InlineKeyboardButton("Check Status", callback_data="check")]
        ]
        await update.message.reply_text("Video lene ke liye pehle sabhi channels join karein:", 
                                        reply_markup=InlineKeyboardMarkup(keyboard))

async def check_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if await is_subscribed(context, query.from_user.id):
        await query.edit_message_text("Thank you! Ab aapko link/video mil jayega.")
    else:
        keyboard = [[InlineKeyboardButton("Check Status Again", callback_data="check")]]
        await query.edit_message_text("Aapne abhi tak saare channels join nahi kiye! Join karne ke baad 'Check Status' dabayein.", 
                                        reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    # TOKEN variable yahan automatically use ho jayega
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(check_callback))
    print("Bot upgraded aur ready hai...")
    application.run_polling()