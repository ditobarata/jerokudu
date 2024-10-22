from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from pustaka import baca_konfigurasi, start, help_command, echo
from handle_location import handle_location
from handle_data_reply import handle_data_reply
from handle_catat_teknisi import catat_teknisi, edit_teknisi_callback, handle_reply
from handle_teks import handle_teks

konf = baca_konfigurasi()

def main():
    # Buat aplikasi bot
    application = Application.builder().token(konf['token_tele']).build()
    application.add_handler(CommandHandler("start", start)) # Tambahkan handler untuk perintah /start
    application.add_handler(CommandHandler("help", help_command)) # Tambahkan handler untuk perintah /help
    application.add_handler(CommandHandler("catat_teknisi", catat_teknisi)) # Tambahkan handler untuk perintah /catat_teknisi
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))# Tambahkan handler untuk pesan tipe Location
    application.add_handler(MessageHandler(filters.REPLY & filters.TEXT, handle_data_reply)) # Tambahkan handler untuk pesan yang membalas dengan kedalaman
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_teks))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo)) # Tambahkan handler untuk semua pesan teks
    application.add_handler(CallbackQueryHandler(edit_teknisi_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply))

    # Jalankan bot
    application.run_polling()

if __name__ == '__main__':
    main()
