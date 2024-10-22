from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from pustaka import insert_location, is_teknisi_terdaftar, tambah_teknisi_otomatis

# Fungsi yang dijalankan ketika bot menerima pesan lokasi dari user
async def handle_location(update: Update, context: CallbackContext) -> None:
    # Mendapatkan informasi koordinat dari pesan lokasi
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    id_telegram = update.message.from_user.id
    nama_teknisi = update.message.from_user.username
    id_pesan = update.message.message_id  # Ambil message_id dari pesan lokasi
    waktu_pelaporan = update.message.date.strftime("%Y-%m-%d %H:%M:%S")  # Format waktu pelaporan
    kedalaman = -1  # nilai fix yang menunjukan bahwa nilai kedalaman blm dimasukkan

    # Simpan data ke database
    location_id = insert_location(latitude, longitude, kedalaman, id_telegram, waktu_pelaporan, id_pesan)

    # Mencetak dan mengirimkan titik koordinat
    await update.message.reply_text(f"Titik koordinat berhasil disimpan dengan ID: {location_id}\n\n"
                                    f"Silahkan reply pesan ini dengan angka untuk mencatatkan kedalaman galian di titik ini "
                                    f"atau dengan pesan bebas untuk mencatatkan keterangan dari galian di titik ini", reply_to_message_id=id_pesan)

    # Periksa apakah teknisi yang mengirim pesan sudah terdaftar
    if not is_teknisi_terdaftar(id_telegram):
        # Jika belum terdaftar, tambahkan teknisi ke tabel teknisi
        tambah_teknisi_otomatis(id_telegram, nama_teknisi)