from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Application
from pustaka import is_admin, baca_konfigurasi
import sqlite3

konf = baca_konfigurasi()

async def catat_teknisi(update, context):
    # Buat koneksi ke database
    conn = sqlite3.connect(konf['database'])
    cursor = conn.cursor()  # Buat cursor dari koneksi

    # Ambil daftar teknisi yang statusnya belum admin (status = 0)
    cursor.execute("SELECT id_telegram, nama FROM teknisi WHERE status IN (0, 2) ORDER BY status DESC")
    teknisi_list = cursor.fetchall()  # Gunakan fetchall() pada objek cursor, bukan connection

    # Buat inline keyboard dari data teknisi
    keyboard = []
    for teknisi in teknisi_list:
        id_telegram, nama = teknisi
        button = InlineKeyboardButton(text=f"{nama}", callback_data=f"edit_{id_telegram}")
        keyboard.append([button])

    # Tutup koneksi database setelah selesai
    cursor.close()
    conn.close()

    # Buat markup dari keyboard yang dibuat dan kirimkan ke pengguna
    reply_markup = InlineKeyboardMarkup(keyboard)
    #await update.message.reply_text("Pilih teknisi yang ingin diedit:", reply_markup=reply_markup)
    await update.message.reply_text("/edit_teknisi0 /edit_teknisi1 /edit_teknisi 2", reply_markup=reply_markup)

async def edit_teknisi_callback(update, context):
    query = update.callback_query
    query_data = query.data

    # Ekstrak ID Telegram teknisi dari callback_data
    if query_data.startswith("edit_"):
        id_telegram = int(query_data.split("_")[1])

        # Kirim pesan untuk mengedit data teknisi tertentu
        await query.edit_message_text(text=f"Anda akan mengedit teknisi dengan ID telegram: {id_telegram}. Silakan copy paste pesan di bawah, diedit sesuai isian yang diinginkan, lalu kirim balik ke saya:")
        await update.message.reply_text(f"nama: \nno_telp: \nloker: ")

        # Simpan ID Telegram ke dalam context untuk akses selanjutnya
        context.user_data['id_telegram'] = id_telegram
    else:
        await query.answer("ID tidak valid.")

async def handle_reply(update, context):
    # Ambil ID Telegram teknisi dari context
    id_telegram = context.user_data.get('id_telegram')
    
    if not id_telegram:
        await update.message.reply_text("ID teknisi tidak ditemukan. Silakan coba lagi.")
        return

    # Ambil balasan dari pengguna
    user_input = update.message.text

    # Cek apakah format balasan benar
    parts = user_input.split("\n")
    
    if len(parts) != 3:
        await update.message.reply_text("Format salah! Mohon masukkan data dalam format: \nnama: \nno_telp: \nloker: ")
        return

    nama, no_telp, loker = parts

    # Update database teknisi
    connection = sqlite3.connect(konf['database'])
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            UPDATE teknisi
            SET nama = ?, no_telp = ?, loker = ?
            WHERE id_telegram = ?
        """, (nama.strip(), no_telp.strip(), loker.strip(), id_telegram))
        
        connection.commit()
        await update.message.reply_text("Data teknisi berhasil diupdate!")
    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan saat mengupdate data: {str(e)}")
    finally:
        connection.close()
