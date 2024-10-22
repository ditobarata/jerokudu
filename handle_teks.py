import sqlite3
from telegram import Update
from telegram.ext import ContextTypes
from pustaka import baca_konfigurasi

konf = baca_konfigurasi()

async def handle_teks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Apabila pesan adalah angka, maka itu adalah nilai kedalaman yang akan dimasukkan ke kolom kedalaman dari data lokasi terakhir
    if update.message.text.isdigit():
        id_telegram = update.message.from_user.id
        id_pesan = update.message.message_id
        kedalaman = int(update.message.text)
        
        # Koneksi ke database
        conn = sqlite3.connect(konf['database'])
        cursor = conn.cursor()
        
        try:
            # Mencari record pertama dengan id_telegram yang belum memiliki kedalaman
            cursor.execute("SELECT id, id_pesan FROM pengecekan WHERE id_telegram = ? AND kedalaman = -1 ORDER BY id DESC LIMIT 1", (id_telegram,))
            record = cursor.fetchone()
            
            if record:
                # Dapatkan id dari record tersebut
                record_id = record[0]
                id_reply = record[1]

                # Update nilai kedalaman di database
                cursor.execute("UPDATE pengecekan SET kedalaman = ? WHERE id = ?", (kedalaman, record_id))
                conn.commit()
                
                # Memberikan konfirmasi kepada pengguna
                await update.message.reply_text(f"Berhasil memasukkan nilai kedalaman: {kedalaman} pada lokasi dengan id: {record_id}.", reply_to_message_id=id_reply)
            else:
                await update.message.reply_text("Tidak ada catatan yang belum memiliki keterangan kedalaman.", reply_to_message_id=id_pesan)
        finally:
            # Tutup koneksi ke database
            conn.close()
    
    # Jika pesan bukan angka, anggap sebagai teks biasa untuk mengisi kolom keterangan
    elif isinstance(update.message.text, str):
        id_telegram = update.message.from_user.id
        id_pesan = update.message.message_id
        keterangan = update.message.text
        
        # Koneksi ke database
        conn = sqlite3.connect(konf['database'])
        cursor = conn.cursor()
        
        try:
            # Mencari record terakhir dengan id_telegram yang belum memiliki keterangan
            cursor.execute("SELECT id, id_pesan FROM pengecekan WHERE id_telegram = ? AND (keterangan IS NULL OR keterangan = '') ORDER BY id DESC LIMIT 1", (id_telegram,))
            record = cursor.fetchone()
            
            if record:
                # Dapatkan id dari record tersebut
                record_id = record[0]
                id_reply = record[1]

                # Update nilai keterangan di database
                cursor.execute("UPDATE pengecekan SET keterangan = ? WHERE id = ?", (keterangan, record_id))
                conn.commit()
                
                # Memberikan konfirmasi kepada pengguna
                await update.message.reply_text(f"Berhasil menambahkan keterangan: {keterangan} pada lokasi dengan id: {record_id}.", reply_to_message_id=id_reply)
            else:
                await update.message.reply_text("Tidak ada catatan yang belum memiliki keterangan.", reply_to_message_id=id_reply)
        finally:
            # Tutup koneksi ke database
            conn.close()
