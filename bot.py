import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, ContextTypes

BOT_TOKEN = "8563248702:AAFacFDVYVYVKpS82DL6S3zRBfIFmNm9mD8"
ADMIN_CHAT_ID = 7534509370
ADMIN_USERNAME = "@Azizjon_Asadov"
LOGO_URL = "https://iili.io/B7rbMGI.png"

PHONE, COMMENT = range(2)

prices = {
    "poster1": "60,000 so‘m",
    "poster4": "102,000 so‘m",
    "video8": "120,000 so‘m",
    "reel": "384,000 so‘m",
    "start": "1,308,000 so‘m",
    "standart": "2,028,000 so‘m",
    "biznes": "4,068,000 so‘m"
}

descriptions = {
    "poster1": "🎨 1 poster (1 variant)",
    "poster4": "🎨 1 poster (4 variant)",
    "video8": "🎬 8 sekund video",
    "reel": "📱 25–30 sekund Reel",
    "start": "🚀 START: 4 Reel + 4 poster",
    "standart": "⭐ STANDART: 6 Reel + 8 poster",
    "biznes": "💼 BIZNES: 12 Reel + 12 poster"
}

def main_menu():
    kb = [
        [InlineKeyboardButton("🎨 AI Dizayn", callback_data="menu_design")],
        [InlineKeyboardButton("🎬 AI Video", callback_data="menu_video")],
        [InlineKeyboardButton("📦 Paketlar", callback_data="menu_packages")],
        [InlineKeyboardButton("📞 Admin bilan bog‘lanish", url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton("ℹ️ Yordam", callback_data="help")]
    ]
    return InlineKeyboardMarkup(kb)

async def start(update: Update, context):
    await update.message.reply_photo(
        photo=LOGO_URL,
        caption=(
            "🤖 *Izdihom AI Media Bot*\n\n"
            "Assalomu alaykum! Quyidagi menyudan xizmat yoki paket tanlang.\n"
            "Telefon raqam va izoh qoldiring, operatorlar tezda bog‘lanadi.\n\n"
            "📞 Admin: @Izdihom_MG"
        ),
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await query.edit_message_caption(caption="Asosiy menyu:", reply_markup=main_menu())
    elif data == "menu_design":
        kb = [[InlineKeyboardButton(f"1 poster (1 var) – {prices['poster1']}", callback_data="poster1")],
              [InlineKeyboardButton(f"1 poster (4 var) – {prices['poster4']}", callback_data="poster4")],
              [InlineKeyboardButton("◀️ Orqaga", callback_data="main_menu")]]
        await query.edit_message_caption(caption="🎨 *AI Dizayn*", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    elif data == "menu_video":
        kb = [[InlineKeyboardButton(f"8 sek video – {prices['video8']}", callback_data="video8")],
              [InlineKeyboardButton(f"Reel 25-30 sek – {prices['reel']}", callback_data="reel")],
              [InlineKeyboardButton("◀️ Orqaga", callback_data="main_menu")]]
        await query.edit_message_caption(caption="🎬 *AI Video*", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    elif data == "menu_packages":
        kb = [[InlineKeyboardButton(f"START – {prices['start']}", callback_data="start")],
              [InlineKeyboardButton(f"STANDART – {prices['standart']} ⭐", callback_data="standart")],
              [InlineKeyboardButton(f"BIZNES – {prices['biznes']}", callback_data="biznes")],
              [InlineKeyboardButton("◀️ Orqaga", callback_data="main_menu")]]
        await query.edit_message_caption(caption="📦 *Oylik paketlar*", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    elif data == "help":
        await query.edit_message_caption(caption="Yordam:\n1. Xizmat tanlang\n2. Telefon raqam\n3. Izoh qoldiring\nOperator bog‘lanadi.", reply_markup=main_menu())
    else:
        context.user_data['selected'] = data
        await query.edit_message_caption(caption=f"✅ Siz tanladingiz: *{descriptions[data]}* – {prices[data]}\n\n📞 Endi telefon raqamingizni yuboring (+998901234567):\nBekor qilish uchun /cancel", parse_mode="Markdown")
        return PHONE

async def phone_handler(update: Update, context):
    phone = update.message.text.strip()
    if not phone.replace("+", "").isdigit() or len(phone) < 9:
        await update.message.reply_text("❌ Noto‘g‘ri format. Qaytadan +998901234567 yuboring yoki /cancel")
        return PHONE
    context.user_data['phone'] = phone
    await update.message.reply_text("📝 Izohingizni yozing (yoki “yo‘q” deb yozing):")
    return COMMENT

async def comment_handler(update: Update, context):
    comment = update.message.text.strip()
    if comment.lower() == "yo‘q":
        comment = "—"
    selected = context.user_data.get('selected')
    phone = context.user_data.get('phone')
    username = update.effective_user.username
    user_mention = f"@{username}" if username else "anonim"
    text = (f"🆕 *YANGI BUYURTMA (bot)* 🆕\n\n"
            f"📦 *Tanlangan:* {descriptions[selected]}\n"
            f"💰 Narxi: {prices[selected]}\n"
            f"📞 Telefon: {phone}\n"
            f"💬 Izoh: {comment}\n"
            f"👤 Foydalanuvchi: {user_mention}\n"
            f"🕒 Vaqt: {update.effective_message.date}")
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text, parse_mode="Markdown")
        await update.message.reply_text("✅ So‘rovingiz qabul qilindi! Operatorlar tezda aloqaga chiqadi.\n\n📞 Admin: @Izdihom_MG", reply_markup=main_menu())
    except Exception:
        await update.message.reply_text("❌ Xatolik. Iltimos, @Izdihom_MG ga yozing.")
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context):
    context.user_data.clear()
    await update.message.reply_text("Bekor qilindi. /start bilan qaytadan boshlang.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern="^(poster1|poster4|video8|reel|start|standart|biznes)$")],
        states={PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_handler)],
                COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, comment_handler)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(menu_design|menu_video|menu_packages|main_menu|help)$"))
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("cancel", cancel))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
