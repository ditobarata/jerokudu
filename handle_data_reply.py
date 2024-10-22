from telegram import Update
from telegram.ext import CallbackContext
from pustaka import update_location_depth, update_location_description, update_location_depth_by_pesan, update_location_description_by_pesan

async def handle_data_reply(update: Update, context: CallbackContext) -> None:
    # Mengambil ID dari pesan yang dibalas
    reply_message = update.message.reply_to_message
    id_pesan = update.message.message_id
    id_pesan_lokasi = reply_message.id
    if reply_message and reply_message.text and reply_message.text.startswith("Titik koordinat berhasil disimpan dengan ID:"): # Jika pengguna mereply pesan yang berupa ID pencatatan lokasi di db
        try:
            # Mengambil ID dari pesan balasan dengan menangani newline
            # Memisahkan teks berdasarkan ":" dan mengambil bagian pertama untuk ID
            location_id = int(reply_message.text.split(":")[1].strip().split("\n")[0])
        except ValueError:
            await update.message.reply_text("ID tidak valid. Silakan balas pesan yang mengandung ID yang benar.", reply_to_message_id=id_pesan_lokasi)
            return

        # Mengambil teks dari pesan yang dibalas
        user_input = update.message.text

        # Memeriksa apakah input adalah angka
        if user_input.isdigit():  # Cek jika input adalah angka
            kedalaman = int(user_input)
            # Memperbarui kolom kedalaman di tabel pengecekan
            update_location_depth(location_id, kedalaman)
            await update.message.reply_text(f"Kedalaman: {kedalaman} berhasil disimpan untuk ID: {location_id}", reply_to_message_id=id_pesan)
        else:
            # Jika bukan angka, simpan sebagai keterangan
            keterangan = user_input
            update_location_description(location_id, keterangan)
            await update.message.reply_text(f"Keterangan: {keterangan} berhasil disimpan untuk ID: {location_id}", reply_to_message_id=id_pesan)
    elif reply_message and reply_message.location: # Jika yang direply pengguna adalah pesan yang berisi lokasi
        # Mengambil teks dari pesan yang dibalas
        user_input = update.message.text
        id_pesan_lokasi = reply_message.id

        # Memeriksa apakah input adalah angka
        if user_input.isdigit():  # Cek jika input adalah angka
            kedalaman = int(user_input)
            # Memperbarui kolom kedalaman di tabel pengecekan
            update_location_depth_by_pesan(id_pesan_lokasi, kedalaman)
            await update.message.reply_text(f"Kedalaman: {kedalaman} berhasil disimpan untuk pesan yang saya reply ini.", reply_to_message_id=id_pesan_lokasi)
        else:
            # Jika bukan angka, simpan sebagai keterangan
            keterangan = user_input
            update_location_description_by_pesan(id_pesan_lokasi, keterangan)
            await update.message.reply_text(f"Keterangan: {keterangan} berhasil disimpan untuk pesan yang saya reply ini.", reply_to_message_id=id_pesan_lokasi)
    else:
        await update.message.reply_text("Silakan balas pesan yang berisi ID untuk menambahkan kedalaman atau keterangan.")
