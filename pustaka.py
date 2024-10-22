from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import sqlite3, yaml

# Fungsi untuk membaca file konfigurasi YAML
def baca_konfigurasi():
    with open("konfig.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

konf = baca_konfigurasi()

# Fungsi yang dijalankan ketika user memulai percakapan dengan bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Halo! Saya adalah jerokudu, bot untuk mencatat infrastruktur kabel anda!")


# Fungsi yang dijalankan ketika user mengirimkan pesan /help
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Saya adalah jerokudu, bot untuk mencatat infrastruktur kabel anda!")

# Fungsi yang dijalankan ketika bot menerima pesan teks dari user
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"jenis pesan tidak dikenal: {update.message.text}")

# Koneksi ke database SQLite
def insert_location(lintang, bujur, kedalaman, id_telegram, waktu_pelaporan, id_pesan):
    konf = baca_konfigurasi()
    conn = sqlite3.connect(konf['database'])
    cursor = conn.cursor()

    # Insert data ke tabel pengecekan
    cursor.execute('''
        INSERT INTO pengecekan (lintang, bujur, kedalaman, id_telegram, waktu_pelaporan, id_pesan) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (lintang, bujur, kedalaman, id_telegram, waktu_pelaporan, id_pesan))

    # Mendapatkan ID yang dihasilkan
    location_id = cursor.lastrowid

    # Commit perubahan dan tutup koneksi
    conn.commit()
    conn.close()
    
    return location_id  # Mengembalikan ID yang dihasilkan

def update_location_depth(id_data, kedalaman):
    konf = baca_konfigurasi()
    conn = sqlite3.connect(konf['database'])
    cursor = conn.cursor()

    # Update kedalaman di tabel pengecekan berdasarkan ID
    cursor.execute('''
        UPDATE pengecekan 
        SET kedalaman = ? 
        WHERE id = ?
    ''', (kedalaman, id_data))

    # Commit perubahan dan tutup koneksi
    conn.commit()
    conn.close()

def update_location_depth_by_pesan(id_data, kedalaman):
    konf = baca_konfigurasi()
    conn = sqlite3.connect(konf['database'])
    cursor = conn.cursor()

    # Update kedalaman di tabel pengecekan berdasarkan ID
    cursor.execute('''
        UPDATE pengecekan 
        SET kedalaman = ? 
        WHERE id_pesan = ?
    ''', (kedalaman, id_data))

    # Commit perubahan dan tutup koneksi
    conn.commit()
    conn.close()

def update_location_description(location_id, keterangan):
    conn = sqlite3.connect(konf['database'])
    cursor = conn.cursor()

    # Memperbarui kolom keterangan berdasarkan ID
    cursor.execute('''
        UPDATE pengecekan
        SET keterangan = ?
        WHERE id = ?
    ''', (keterangan, location_id))

    conn.commit()
    conn.close()

def update_location_description_by_pesan(location_id, keterangan):
    conn = sqlite3.connect(konf['database'])
    cursor = conn.cursor()

    # Memperbarui kolom keterangan berdasarkan ID
    cursor.execute('''
        UPDATE pengecekan
        SET keterangan = ?
        WHERE id_pesan = ?
    ''', (keterangan, location_id))

    conn.commit()
    conn.close()

def is_teknisi_terdaftar(id_telegram: int) -> bool:
    conn = sqlite3.connect("kabel_tanah.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM teknisi WHERE id_telegram = ?", (id_telegram,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Fungsi untuk menambahkan teknisi baru secara otomatis ke database
def tambah_teknisi_otomatis(id_telegram: int, username: str):
    conn = sqlite3.connect("kabel_tanah.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO teknisi (id_telegram, nama, no_telp, loker, status) VALUES (?, ?, ?, ?, ?)",
        (id_telegram, username, "", "", 0),  # No_telp kosong, loker kosong, admin = 0
    )
    conn.commit()
    conn.close()

# Fungsi untuk memeriksa apakah user adalah admin
def is_admin(user_id: int) -> bool:
    print(f"User ID: {user_id}, Type: {type(user_id)}")
    conn = sqlite3.connect(konf['database'])
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM teknisi WHERE id_telegram = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result is not None and result[0] == 1